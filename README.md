# 漫威争锋 · 自动挂机脚本 / Marvel Rivals Auto-Farm Script

---

## 中文版

### 免责声明

1. **本脚本仅供学习与技术交流**，用于研究屏幕图像识别与键鼠模拟原理。
2. **使用自动化脚本可能违反《漫威争锋》或平台的用户协议**，存在账号警告、限制或封禁等风险。是否使用、如何使用，**完全由你本人承担全部责任**。
3. 作者及贡献者**不对**因使用本脚本导致的任何直接或间接损失负责，包括但不限于：账号封禁、进度损失、设备异常、数据损坏等。
4. 请勿将本脚本用于商业用途，勿传播用于破坏游戏公平性的用途。
5. 游戏版本、UI、分辨率更新后，模板可能失效；维护与适配需自行负责。
6. **继续使用即视为你已阅读并同意以上全部条款。**

---

### 脚本做什么

基于 **屏幕截图 + 模板匹配 + 键鼠模拟**，在**游戏前台、管理员权限**下自动循环：

1. 主页点击「开始游戏」
2. 选人页：有「索尔」则点「确定」；没有则先点索尔头像再确定；若已是「取消」则等待进图
3. 局内：仅当右下角 **F 为「待使用」** 时按 F（使用中 / 冷却中不按）
4. 结算：结束页长按空格跳过 → 再按 ESC 回主页 → 循环

**不是**读内存、不是注入、不支持真正后台挂机（游戏一般需在前台）。

---

### 使用前必须满足的条件

#### 关卡与模式

| 项目 | 要求 |
|------|------|
| 主页模式 | 运行前须在主页**手动选好「血猎」模式**（脚本不会帮你切模式） |
| 难度 | **噩梦 1（Nightmare 1）** |
| 说明 | 其它模式 / 难度 UI 与流程不同，脚本未适配 |

#### 英雄与养成（强烈建议）

| 项目 | 要求 |
|------|------|
| 英雄 | **索尔（Thor / 雷神）** |
| 伤害 | **足够高**，能在 F 技能挂机节奏下清怪、推进波次 |
| 生命 / 生存 | **足够高**，避免被怪物打死导致流程中断 |
| 说明 | 脚本**不会**走位、不会治疗、不会操作其它技能；过脆或过弱极易卡关或失败 |

#### 运行环境

| 项目 | 要求 |
|------|------|
| 系统 | Windows |
| Python | 3.10+ 推荐 |
| 权限 | **管理员身份**运行终端（否则游戏内点击/按键常无效） |
| 窗口 | 游戏**前台**、不被其它窗口遮挡 |
| 分辨率 | 参考 **2559×1439**（接近 2560×1440）；脚本会尝试缩放，但差太多需自备模板 |
| 依赖 | 见 `requirements.txt` |

---

### 安装与运行

```powershell
cd E:\mr
pip install -r requirements.txt

# 务必：右键「以管理员身份运行」PowerShell / 终端后再执行
python .\auto_farm.py
```

快捷键：

| 键 | 功能 |
|----|------|
| F9 | 开始 / 继续 |
| F10 | 暂停 |
| F11 | 退出 |

启动后约 3 秒倒计时，请先切到游戏窗口。

---

### 目录说明

```
templates/
  detect/     # 判断当前页面 / 状态（含 F 三态、索尔名字等）
  click/      # 点击目标（开始游戏、索尔头像、确定、取消等）
```

---

### 风险与限制（请知悉）

- 必须游戏在前台；切走窗口可能导致误点桌面或其它程序。
- UI、皮肤、语言、分辨率变化会导致识别失败。
- 局内只管理 F 技能状态，**不保证通关**；养成不足时请先手动练度。
- 反作弊或协议变更可能导致账号风险——**再次强调：后果自负**。

---

## English

> Localization note: Proper nouns below follow **Marvel Rivals** English client / official patch & community usage (e.g. NetEase patch notes, Blood Hunt guides).  
> This repo’s templates were captured from the **Simplified Chinese** client—UI pixel matching still expects Chinese strings on screen unless you replace templates.

### Glossary (CN → EN)

| Chinese (in-game) | English (localized) | Notes |
|-------------------|---------------------|--------|
| 漫威争锋 | **Marvel Rivals** | Official title |
| 血猎 | **Blood Hunt** | Limited-time **PvE** mode |
| 噩梦 1 | **Nightmare 1** | Nightmare ladder tier; patch notes also say **Floor** (e.g. Floor 300). Same as community **NM 1** |
| 索尔 / 雷神索尔 | **Thor** | Official hero name (Thor Odinson) |
| 开始游戏 | **Start** | Yellow lobby queue button (nav tab is often **Play**) |
| 确定 | **Confirm** | Hero lock-in |
| 取消 | **Cancel** | Shown after Confirm; same slot |
| 长按跳过全部 | **Long press to skip all** | Results screen (Space) |
| 待使用 / 使用中 / 冷却中 | **Ready** / **Active** / **On cooldown** | Script labels for the **F** ability icon states |

Difficulty ladder in Blood Hunt (official English): **Normal → Hard → Extreme → Nightmare**.

---

### Disclaimer

1. This script is provided **for learning and technical research only** (screen matching and input simulation).
2. Using automation may **violate the Marvel Rivals Terms of Service** (and related platform rules) and may result in warnings, restrictions, or bans. **You assume all risk and responsibility.**
3. Authors and contributors are **not liable** for any loss arising from use of this script, including but not limited to account bans, progress loss, device issues, or data damage.
4. Do not use commercially or to undermine fair play.
5. Game / UI / resolution updates may break templates; maintenance is your responsibility.
6. **By using this script, you acknowledge and agree to the above.**

---

### What it does

**Screenshot → template matching → keyboard/mouse simulation**, with Marvel Rivals in the **foreground** and the script run as **Administrator**:

1. Lobby: click **Start**
2. Hero select: if **Thor** is selected, click **Confirm**; if not, select Thor then **Confirm**; if **Cancel** is shown, wait for the match to begin
3. In match: press **F** only when that ability is **Ready** (not while **Active** or **on cooldown**)
4. Results: long-press **Space** (**Long press to skip all**) → press **Esc** to return to the lobby → loop

This is **not** memory reading or injection, and **not** true background AFK (the game usually must stay focused).

---

### Requirements before use

#### Mode / difficulty

| Item | Requirement |
|------|-------------|
| Mode | On the lobby (home) screen, **manually select Blood Hunt** before running—the script does **not** change modes |
| Difficulty | **Nightmare 1** (Nightmare Floor 1 / NM 1) |
| Note | Other modes or Nightmare floors are **not** supported |

#### Hero / build (strongly recommended)

| Item | Requirement |
|------|-------------|
| Hero | **Thor** |
| Damage | **High enough** to clear vampire waves under F-based AFK pacing |
| Health / survivability | **High enough** so you are not downed by trash mobs |
| Note | The script does **not** move, heal, or use other abilities. A weak Blood Hunt loadout will fail or stall. |

#### Runtime

| Item | Requirement |
|------|-------------|
| OS | Windows |
| Python | 3.10+ recommended |
| Privileges | Run the terminal **as Administrator** |
| Window | Game **in foreground**, not occluded |
| Resolution | Reference **2559×1439** (~1440p); scaling is attempted, but large mismatches need new templates |
| Client language | Templates target the **Simplified Chinese** UI unless you replace them |
| Dependencies | See `requirements.txt` |

---

### Install & run

```powershell
cd E:\mr
pip install -r requirements.txt

# Important: open PowerShell / terminal as Administrator
python .\auto_farm.py
```

Hotkeys:

| Key | Action |
|-----|--------|
| F9 | Start / resume |
| F10 | Pause |
| F11 | Quit |

After launch there is a ~3s countdown—switch to the Marvel Rivals window first.

---

### Layout

```
templates/
  detect/     # page / state detection (incl. F states, Thor name)
  click/      # click targets (Start, Thor icon, Confirm, Cancel, etc.)
```

---

### Limitations

- The game must stay in the foreground; switching away may click the wrong window.
- UI, costumes, language, or resolution changes can break recognition.
- Only the **F** Ready state is managed in combat—**clearing Blood Hunt is not guaranteed**.
- Anti-cheat / ToS changes may affect your account—**use at your own risk**.
