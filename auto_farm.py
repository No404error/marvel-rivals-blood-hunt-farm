# -*- coding: utf-8 -*-
"""
漫威争锋 自动挂机脚本

流程：
  主页[开始游戏] → 选人[索尔+确定]
  → 游戏中：仅当右下角 F 为「待使用」时按 F（使用中/冷却中不按）
  → 结束1[长按空格跳过全部] → 结束2[ESC 回主页] → 循环

使用前请确保：
  1. 游戏分辨率为 2559x1439（与参考截图一致），或设置 SCALE 缩放
  2. 游戏窗口在前台、未被遮挡
  3. 必须以管理员身份运行

快捷键：
  F9  - 开始/继续自动化
  F10 - 暂停
  F11 - 退出
"""

from __future__ import annotations

import os
import sys
import time
import threading
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import cv2
import mss
import numpy as np
import pydirectinput
import pyautogui

# 禁用 pyautogui 角落 fail-safe，避免鼠标移到屏幕角落时中断
pyautogui.FAILSAFE = False
pydirectinput.PAUSE = 0.05

def _app_base_dir() -> Path:
    """开发时用源码目录；打包成 exe 后用 PyInstaller 解压目录（模板已内嵌）。"""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent


BASE_DIR = _app_base_dir()
# detect/ = 判断当前页面；click/ = 点击目标。两者严格分离。
DETECT_DIR = BASE_DIR / "templates" / "detect"
CLICK_DIR = BASE_DIR / "templates" / "click"

# 参考截图分辨率；若游戏分辨率不同，脚本会自动等比缩放坐标与模板
REF_WIDTH = 2559
REF_HEIGHT = 1439

MATCH_THRESHOLD = 0.72
POLL_INTERVAL = 0.8
ACTION_DELAY = 1.2
LOAD_TIMEOUT = 120
SPACE_HOLD_SECONDS = 1.8  # 结束1：长按空格跳过全部
F_STATE_MARGIN = 0.05  # 待使用须比其它 F 状态高出该差值才按


class Page(Enum):
    UNKNOWN = auto()
    MAIN = auto()
    HERO_SELECT = auto()
    IN_GAME = auto()
    END1 = auto()
    END2 = auto()


class FState(Enum):
    UNKNOWN = auto()
    READY = auto()  # 待使用
    USING = auto()  # 使用中
    COOLDOWN = auto()  # 冷却中


class BotState(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()


@dataclass
class MatchResult:
    page: Page
    confidence: float
    center: tuple[int, int] | None


@dataclass
class FStateResult:
    state: FState
    confidence: float
    scores: dict[str, float]


def imread_unicode(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"无法读取图片: {path}")
    return img


class ScreenMatcher:
    def __init__(self) -> None:
        self.detect_templates: dict[Page, np.ndarray] = {}
        self.click_templates: dict[str, np.ndarray] = {}
        self.f_templates: dict[FState, np.ndarray] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        detect_map = {
            Page.MAIN: "main.png",
            Page.HERO_SELECT: "hero_select.png",
            Page.IN_GAME: "in_game.png",
            Page.END1: "end1.png",
            Page.END2: "end2.png",
        }
        for page, filename in detect_map.items():
            path = DETECT_DIR / filename
            if path.exists():
                self.detect_templates[page] = imread_unicode(path)

        for name in ("start_game.png", "confirm.png", "cancel.png", "thor.png"):
            path = CLICK_DIR / name
            if path.exists():
                self.click_templates[name] = imread_unicode(path)

        # 选人页左下「索尔」——判断是否已选中（非点击目标）
        thor_name_path = DETECT_DIR / "thor_name.png"
        self.thor_name_template = (
            imread_unicode(thor_name_path) if thor_name_path.exists() else None
        )

        f_dir = DETECT_DIR / "f"
        f_map = {
            FState.READY: "ready.png",
            FState.USING: "using.png",
            FState.COOLDOWN: "cooldown.png",
        }
        for state, filename in f_map.items():
            path = f_dir / filename
            if path.exists():
                self.f_templates[state] = imread_unicode(path)

        if not self.detect_templates:
            raise RuntimeError(f"未找到状态模板，请确认 {DETECT_DIR} 目录存在")
        if not self.click_templates:
            raise RuntimeError(f"未找到点击模板，请确认 {CLICK_DIR} 目录存在")
        if not self.f_templates:
            raise RuntimeError(f"未找到 F 技能模板，请确认 {f_dir} 目录存在")

    def capture_screen(self) -> np.ndarray:
        with mss.MSS() as sct:
            monitor = sct.monitors[1]
            shot = sct.grab(monitor)
            frame = np.array(shot)
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    def _scale_template(
        self, template: np.ndarray, full_w: int, full_h: int
    ) -> np.ndarray:
        scale_w = full_w / REF_WIDTH
        scale_h = full_h / REF_HEIGHT
        scale = min(scale_w, scale_h)
        if abs(scale - 1.0) < 0.02:
            return template
        new_w = max(8, int(template.shape[1] * scale))
        new_h = max(8, int(template.shape[0] * scale))
        return cv2.resize(template, (new_w, new_h), interpolation=cv2.INTER_AREA)

    def match_template(
        self,
        screen: np.ndarray,
        template: np.ndarray,
        *,
        full_size: tuple[int, int] | None = None,
    ) -> tuple[float, tuple[int, int] | None]:
        sh, sw = screen.shape[:2]
        fw, fh = full_size if full_size else (sw, sh)
        tpl = self._scale_template(template, fw, fh)
        th, tw = tpl.shape[:2]
        if th > sh or tw > sw:
            return 0.0, None

        result = cv2.matchTemplate(screen, tpl, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        cx = max_loc[0] + tw // 2
        cy = max_loc[1] + th // 2
        return float(max_val), (cx, cy)

    def detect_page(self, screen: np.ndarray) -> MatchResult:
        best = MatchResult(Page.UNKNOWN, 0.0, None)
        for page, template in self.detect_templates.items():
            conf, center = self.match_template(screen, template)
            if conf > best.confidence:
                best = MatchResult(page, conf, center)
        if best.confidence >= MATCH_THRESHOLD:
            return best
        return MatchResult(Page.UNKNOWN, best.confidence, None)

    def find_click_target(
        self, screen: np.ndarray, template_name: str
    ) -> tuple[int, int] | None:
        template = self.click_templates.get(template_name)
        if template is None:
            return None
        conf, center = self.match_template(screen, template)
        if conf >= MATCH_THRESHOLD and center:
            return center
        return None

    def has_thor_selected(self, screen: np.ndarray) -> tuple[bool, float]:
        """选人页左下是否出现「索尔」二字。"""
        if self.thor_name_template is None:
            return False, 0.0
        h, w = screen.shape[:2]
        # 左下区域搜索
        roi = screen[int(h * 0.55) : h, 0 : int(w * 0.45)]
        conf, _ = self.match_template(roi, self.thor_name_template, full_size=(w, h))
        return conf >= MATCH_THRESHOLD, conf

    def detect_hero_action_button(
        self, screen: np.ndarray
    ) -> tuple[str | None, float, tuple[int, int] | None]:
        """识别选人页右侧动作按钮：confirm / cancel / None。"""
        best_name: str | None = None
        best_conf = 0.0
        best_pos: tuple[int, int] | None = None
        for name in ("confirm.png", "cancel.png"):
            tpl = self.click_templates.get(name)
            if tpl is None:
                continue
            conf, pos = self.match_template(screen, tpl)
            if conf > best_conf:
                best_conf = conf
                best_pos = pos
                best_name = name.replace(".png", "")
        if best_conf < MATCH_THRESHOLD:
            return None, best_conf, None
        return best_name, best_conf, best_pos

    def detect_f_state(self, screen: np.ndarray) -> FStateResult:
        """在右下角技能栏匹配 F 三态，取最高分者。"""
        h, w = screen.shape[:2]
        # 只在右下角搜索；缩放仍按全屏分辨率，避免 ROI 导致比例错误
        roi = screen[int(h * 0.75) : h, int(w * 0.75) : w]
        scores: dict[str, float] = {}
        best_state = FState.UNKNOWN
        best_conf = 0.0
        for state, template in self.f_templates.items():
            conf, _ = self.match_template(roi, template, full_size=(w, h))
            scores[state.name.lower()] = conf
            if conf > best_conf:
                best_conf = conf
                best_state = state

        if best_conf < MATCH_THRESHOLD:
            return FStateResult(FState.UNKNOWN, best_conf, scores)

        # 待使用须明显优于其它状态，避免和「使用中」混淆
        others = [v for k, v in scores.items() if k != best_state.name.lower()]
        second = max(others) if others else 0.0
        if best_state == FState.READY and best_conf - second < F_STATE_MARGIN:
            return FStateResult(FState.UNKNOWN, best_conf, scores)

        return FStateResult(best_state, best_conf, scores)


class AutoFarmBot:
    def __init__(self) -> None:
        self.matcher = ScreenMatcher()
        self.state = BotState.IDLE
        self.step_done = {
            "selected_hero": False,
            "confirmed_hero": False,
            "pressed_f": False,
        }
        self._last_click_at = 0.0
        self._click_cooldown = 2.5
        self._lock = threading.Lock()

    def log(self, msg: str) -> None:
        print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

    def click(self, x: int, y: int) -> None:
        """游戏窗口优先用 DirectInput 点击，提高全屏下命中率。"""
        now = time.time()
        if now - self._last_click_at < self._click_cooldown:
            self.log(f"点击冷却中，跳过 ({x}, {y})")
            return
        self._last_click_at = now
        pydirectinput.moveTo(x, y)
        time.sleep(0.05)
        pydirectinput.click()
        time.sleep(ACTION_DELAY)

    def press_f(self) -> None:
        now = time.time()
        if now - self._last_click_at < self._click_cooldown:
            self.log("按键冷却中，跳过 F")
            return
        self._last_click_at = now
        pydirectinput.press("f")
        time.sleep(ACTION_DELAY)

    def hold_space(self, seconds: float = SPACE_HOLD_SECONDS) -> None:
        now = time.time()
        if now - self._last_click_at < self._click_cooldown:
            self.log("按键冷却中，跳过长按空格")
            return
        self._last_click_at = now
        self.log(f"结束1：长按空格 {seconds:.1f}s 跳过全部")
        pydirectinput.keyDown("space")
        time.sleep(seconds)
        pydirectinput.keyUp("space")
        time.sleep(ACTION_DELAY)

    def press_esc(self) -> None:
        now = time.time()
        if now - self._last_click_at < self._click_cooldown:
            self.log("按键冷却中，跳过 ESC")
            return
        self._last_click_at = now
        self.log("结束2：按下 ESC 返回主页")
        pydirectinput.press("esc")
        time.sleep(ACTION_DELAY)

    def reset_cycle(self) -> None:
        self.step_done = {
            "selected_hero": False,
            "confirmed_hero": False,
            "pressed_f": False,
        }

    def handle_main(self, screen: np.ndarray) -> bool:
        # 回到主页时允许重新选人/确定
        self.step_done["selected_hero"] = False
        self.step_done["confirmed_hero"] = False
        # 仍在主页就持续尝试点「开始游戏」（避免点了一次没进就卡住）
        pos = self.matcher.find_click_target(screen, "start_game.png")
        if pos:
            self.log(f"主页：点击「开始游戏」 {pos}")
            self.click(*pos)
            return True
        self.log("主页：未找到「开始游戏」按钮，等待中…")
        return False

    def handle_hero_select(self, screen: np.ndarray) -> bool:
        has_thor, name_conf = self.matcher.has_thor_selected(screen)
        btn, btn_conf, btn_pos = self.matcher.detect_hero_action_button(screen)

        # 有索尔 + 取消 → 已锁定，只等待进图
        if has_thor and btn == "cancel":
            self.step_done["selected_hero"] = True
            self.step_done["confirmed_hero"] = True
            self.log(
                f"选人页：已有「索尔」+「取消」（{name_conf:.2f}/{btn_conf:.2f}）→ 等待进图"
            )
            return False

        # 还没选索尔 → 先点头像
        if not has_thor:
            self.log(f"选人页：未看到「索尔」（置信度 {name_conf:.2f}）→ 先点头像")
            thor_pos = self.matcher.find_click_target(screen, "thor.png")
            if not thor_pos:
                self.log("选人页：未找到索尔头像，等待中…")
                return False
            self.log(f"选人页：选择索尔 {thor_pos}")
            self.click(*thor_pos)
            self.step_done["selected_hero"] = True
            return True

        # 有索尔 + 确定 → 点击确定
        if btn == "confirm" and btn_pos:
            self.log(
                f"选人页：已有「索尔」+「确定」（{name_conf:.2f}/{btn_conf:.2f}）→ 点击确定 {btn_pos}"
            )
            self.click(*btn_pos)
            self.step_done["selected_hero"] = True
            self.step_done["confirmed_hero"] = True
            return True

        self.log(
            f"选人页：有「索尔」但按钮不明（thor={name_conf:.2f}, btn={btn}/{btn_conf:.2f}），等待…"
        )
        return False

    def handle_in_game(self, screen: np.ndarray) -> bool:
        self.step_done["pressed_f"] = True  # 标记本局已进过图，回主页时重置
        f_result = self.matcher.detect_f_state(screen)
        scores_txt = " ".join(f"{k}={v:.2f}" for k, v in f_result.scores.items())
        if f_result.state == FState.READY:
            self.log(f"游戏中：F 待使用（{scores_txt}）→ 按 F")
            self.press_f()
            return True
        if f_result.state == FState.USING:
            self.log(f"游戏中：F 使用中（{scores_txt}）")
        elif f_result.state == FState.COOLDOWN:
            self.log(f"游戏中：F 冷却中（{scores_txt}）")
        else:
            self.log(f"游戏中：F 状态不明（{scores_txt}）")
        return False

    def handle_end1(self) -> bool:
        self.hold_space()
        return True

    def handle_end2(self) -> bool:
        self.press_esc()
        return True

    def tick(self) -> None:
        with self._lock:
            if self.state != BotState.RUNNING:
                return

        screen = self.matcher.capture_screen()
        page_result = self.matcher.detect_page(screen)

        if page_result.page == Page.UNKNOWN:
            self.log(f"未识别页面（最高置信度 {page_result.confidence:.2f}），等待中…")
            return

        self.log(f"当前页面：{page_result.page.name}（置信度 {page_result.confidence:.2f}）")

        if page_result.page == Page.MAIN:
            if self.step_done["pressed_f"]:
                self.log("检测到回到主页，开始新一轮")
                self.reset_cycle()
            # 回到主页说明上一轮选人未完成，允许重选
            self.step_done["selected_hero"] = False
            self.handle_main(screen)
        elif page_result.page == Page.HERO_SELECT:
            self.handle_hero_select(screen)
        elif page_result.page == Page.IN_GAME:
            self.handle_in_game(screen)
        elif page_result.page == Page.END1:
            self.handle_end1()
        elif page_result.page == Page.END2:
            self.handle_end2()

    def run_loop(self) -> None:
        while True:
            with self._lock:
                if self.state == BotState.STOPPED:
                    break
                running = self.state == BotState.RUNNING
            if running:
                try:
                    self.tick()
                except Exception as exc:
                    self.log(f"错误: {exc}")
            time.sleep(POLL_INTERVAL)

    def start(self) -> None:
        with self._lock:
            if self.state == BotState.STOPPED:
                return
            self.state = BotState.RUNNING
        self.log(">>> 开始运行")

    def pause(self) -> None:
        with self._lock:
            if self.state == BotState.STOPPED:
                return
            self.state = BotState.PAUSED
        self.log(">>> 已暂停（按 F9 继续）")

    def stop(self) -> None:
        with self._lock:
            self.state = BotState.STOPPED
        self.log(">>> 已退出")


def setup_hotkeys(bot: AutoFarmBot) -> None:
    import keyboard

    keyboard.add_hotkey("f9", bot.start)
    keyboard.add_hotkey("f10", bot.pause)
    keyboard.add_hotkey("f11", bot.stop)


def is_running_as_admin() -> bool:
    """检测当前进程是否已提升（真正的管理员令牌），不能只用 IsUserAnAdmin。"""
    try:
        import ctypes
        from ctypes import wintypes

        class TOKEN_ELEVATION(ctypes.Structure):
            _fields_ = [("TokenIsElevated", wintypes.DWORD)]

        TOKEN_QUERY = 0x0008
        TokenElevation = 20

        advapi32 = ctypes.windll.advapi32
        kernel32 = ctypes.windll.kernel32

        token = wintypes.HANDLE()
        if not advapi32.OpenProcessToken(
            kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(token)
        ):
            return False

        elevation = TOKEN_ELEVATION()
        ret_len = wintypes.DWORD()
        ok = advapi32.GetTokenInformation(
            token,
            TokenElevation,
            ctypes.byref(elevation),
            ctypes.sizeof(elevation),
            ctypes.byref(ret_len),
        )
        kernel32.CloseHandle(token)
        if not ok:
            return False
        return bool(elevation.TokenIsElevated)
    except Exception:
        try:
            import ctypes

            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False


def require_admin() -> None:
    """必须以管理员身份运行，否则键鼠无法作用于游戏。"""
    import ctypes

    elevated = is_running_as_admin()
    print(f"管理员权限检测（进程已提升）: {'是' if elevated else '否'}")
    if elevated:
        print("管理员权限：已确认")
        return

    msg = (
        "必须使用管理员权限运行本程序。\n\n"
        "请关闭后重新运行：\n"
        "· exe：双击后在 UAC 窗口点「是」\n"
        "· 或右键 exe → 以管理员身份运行\n"
        "· Python：右键终端 → 以管理员身份运行"
    )
    print("=" * 50)
    print("  错误：未检测到管理员权限（进程未提升）")
    print("=" * 50)
    print(msg)
    print()
    try:
        ctypes.windll.user32.MessageBoxW(0, msg, "漫威争锋自动挂机", 0x10)
    except Exception:
        pass
    try:
        input("按回车键退出…")
    except EOFError:
        time.sleep(8)
    sys.exit(1)


def main() -> None:
    print("=" * 50)
    print("  漫威争锋 自动挂机")
    print("=" * 50)
    print()
    require_admin()
    print()

    try:
        import keyboard
    except ImportError:
        print("缺少 keyboard 库，正在安装…")
        os.system(f'"{sys.executable}" -m pip install keyboard -q')
        import keyboard

    print("流程：主页 → 选人 → 局内F待使用才按 → 结束1长按空格 → 结束2按ESC → 循环")
    print()
    print("快捷键：")
    print("  F9  - 开始 / 继续")
    print("  F10 - 暂停")
    print("  F11 - 退出")
    print()

    bot = AutoFarmBot()

    with mss.MSS() as sct:
        mon = sct.monitors[1]
        sw, sh = mon["width"], mon["height"]
        print(f"当前屏幕分辨率: {sw}x{sh}（参考: {REF_WIDTH}x{REF_HEIGHT}）")
        if abs(sw / sh - REF_WIDTH / REF_HEIGHT) > 0.05:
            print("警告：屏幕比例与参考截图不同，识别可能不准确")

    print()
    print("请切到游戏窗口，3 秒后自动开始…")
    for i in range(3, 0, -1):
        print(f"  {i}…")
        time.sleep(1)

    setup_hotkeys(bot)
    bot.start()
    bot.run_loop()


if __name__ == "__main__":
    main()
