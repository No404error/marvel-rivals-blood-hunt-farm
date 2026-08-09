# 漫威争锋 · 血猎自动挂机 / Marvel Rivals · Blood Hunt Auto-Farm

**语言 / Language：** [中文](#zh) · [English](#en)

本仓库是一个 **[ScreenFlow](https://github.com/No404error/screenflow-studio)** **项目实例**（配置 + 识别资源），用于在《漫威争锋》**血猎**模式下前台自动挂机。  
**不包含** ScreenFlow 引擎；请用 ScreenFlow（Web Studio）打开本文件夹后运行。

This repository is a **[ScreenFlow](https://github.com/No404error/screenflow-studio)** **project pack** (config + vision assets) for foreground auto-farming Marvel Rivals **Blood Hunt**.  
It does **not** include the ScreenFlow engine — open this folder in ScreenFlow (Web Studio) to run it.

---

<a id="zh"></a>

## 中文文档

**[English](#en)**

### 概述

在游戏保持**前台**时，用截屏 + 模板匹配识别界面，并模拟键鼠，大致循环：

1. 主页点击开始游戏  
2. 若装备过多：角色培养 → 锻炉 → 全选 → 熔炼 → 确认奖励后回主页  
3. 选人：有索尔则确定；没有则先点索尔再确定  
4. 局内：右下角 F 为「待使用」时按 F  
5. 结算：跳过 → 回主页 → 再开一局  

不是读内存、不是注入；游戏不在前台时无法可靠运行。

### 重要：资源面向简体中文客户端

`pages/` 下的画面特征、匹配裁切与文案相关匹配，均按 **简体中文** UI、约 **2560×1440** 采集。

- **英文或其其它语言客户端不能直接套用**这些图与部分情况条件。  
- 请对照下方挂机逻辑，在 Studio 中自行重配页面、情况树、画面特征 / 匹配方案后再运行。  
- 分辨率差得较远或 UI 改版后，同样需要重新截取原图并调整匹配方案。

### 前置条件

本项目**不会**自动切换模式或难度。开始前请同时满足：

| 类别 | 条件 |
|------|------|
| 软件 | 已安装并可启动 [ScreenFlow](https://github.com/No404error/screenflow-studio)（Windows） |
| 系统 | 默认**提权外部引擎**可能弹出 UAC，需允许；也可在 Studio 中改用 **inline（进程内）** |
| 游戏模式 | 主页已手动选好 **血猎** |
| 难度 | **噩梦 1** |
| 队伍 | **单人**（不要组队 / 匹配补齐队友） |
| 客户端语言 | **简体中文**（与仓库资源一致；其它语言须自行重配） |
| 分辨率 | 资源基于约 **2560×1440**；差得较远时请自行重截并重配 |
| 运行时 | 游戏窗口保持**前台**；选人逻辑按 **索尔** 编写 |

不满足难度 / 模式 / 语言时，识别与流程很容易失败。

### 怎么用

1. 安装并启动 ScreenFlow  
   - 仓库：[No404error/screenflow-studio](https://github.com/No404error/screenflow-studio)  
   - 打包版：启动 `release/ScreenFlow.exe`（托盘 + 浏览器打开 Web Studio）  
   - 源码开发：见引擎仓库 README（如 `python .\run_web_studio.py`）  
2. 在 Studio 中打开**本仓库根目录**（含 `project.json` 与 `pages/` 的那一层）。  
3. 确认上一节前置条件（尤其是 **血猎 + 噩梦 1 + 单人 + 简体中文**）。  
4. 按需微调运行参数后 **保存**，再点 **开始**。用暂停 / 继续 / 停止控制运行。  

关掉浏览器标签**不会**退出 ScreenFlow；正式退出请用托盘「退出」或网页上的「退出 ScreenFlow」。界面语言、最近项目、引擎运行模式等保存在用户目录，例如：

```text
C:\Users\<用户名>\.screenflow\ui.json
```

不属于本仓库。

### 目录说明

本包遵循 ScreenFlow 项目模型（画面特征 / 原图 / 匹配方案）：

```text
.
├── project.json              # 运行参数、页面列表、变量等
├── pages/{页面 id}/
│   ├── page.json             # 画面特征、原图、匹配方案、识别引用、情况树、动作、后续观察
│   ├── sources/              # 页级原图（整窗截图；Studio 素材）
│   └── features/             # 匹配方案派生的裁切小图（运行时模板）
└── README.md                 # 本说明（中英合一）
```

页面大致包括：主页、角色培养、锻炉、熔炼确认、恭喜获得、选人、局内、结算等。

更完整的引擎概念（情况树、后续观察、脚本步骤、Web Studio 用法）见 [ScreenFlow README](https://github.com/No404error/screenflow-studio)。

### 免责声明

本项目仅供学习与技术交流。使用自动化可能违反游戏或平台用户协议，存在封号等风险，**后果自负**。作者不对任何损失负责。请在合法合规前提下使用。

### 相关链接

- 引擎 / Studio：[screenflow-studio](https://github.com/No404error/screenflow-studio)

---

<a id="en"></a>

## English

**[中文](#zh)**

### Overview

With the game in the **foreground**, this pack uses screen capture + template matching and simulated input to loop roughly:

1. On the main screen, click Start  
2. If gear is full: Character Maintenance → Forge → select all → melt → confirm rewards → back to main  
3. Hero select: if Thor is already shown, confirm; otherwise pick Thor then confirm  
4. In match: press **F** only when the bottom-right F prompt is “ready”  
5. Results: skip → back to main → start again  

No memory reading, no injection. Background (non-foreground) play is not supported.

### Important: assets are for Simplified Chinese UI

Screen features, match crops, and text-dependent matches under `pages/` were captured from the **Simplified Chinese** client at about **2560×1440**.

- **English (or any other language) clients will not work with these assets as-is.**  
- Use the farm logic above as a guide, then reconfigure pages, case trees, screen features / match setups in Studio before running.  
- If your resolution differs a lot, or the UI changes, recapture originals and adjust match setups the same way.

### Prerequisites

This pack does **not** change mode or difficulty for you. Meet **all** of the following:

| Category | Requirement |
|----------|-------------|
| Software | [ScreenFlow](https://github.com/No404error/screenflow-studio) installed and runnable (Windows) |
| OS | Default **elevated external runner** may show UAC; you can switch to **inline** in Studio |
| Game mode | **Blood Hunt** already selected on the main screen |
| Difficulty | **Nightmare 1** |
| Party | **Solo** (no party / fill teammates) |
| Client language | **Simplified Chinese** (matches bundled assets; other languages need your own reconfiguration) |
| Resolution | Assets were captured around **2560×1440**; recapture and reconfigure if yours differs a lot |
| Runtime | Keep the game **in the foreground**; hero flow is written for **Thor** |

Wrong difficulty, mode, or UI language will usually break detection and the loop.

### How to use

1. Install and launch ScreenFlow  
   - Repository: [No404error/screenflow-studio](https://github.com/No404error/screenflow-studio)  
   - Packaged: run `release/ScreenFlow.exe` (tray + browser opens Web Studio)  
   - From source: see the engine repo README (e.g. `python .\run_web_studio.py`)  
2. In Studio, open **this repository root** (the folder with `project.json` and `pages/`).  
3. Confirm the prerequisites above (especially **Blood Hunt + Nightmare 1 + solo + Simplified Chinese**).  
4. Tweak run settings if needed, **Save**, then **Start**. Use Pause / Continue / Stop as needed.  

Closing the browser tab does **not** quit ScreenFlow; exit via the tray or **Quit ScreenFlow** in the web UI. UI language, recent projects, runner mode, and similar prefs live under the user profile, for example:

```text
C:\Users\<you>\.screenflow\ui.json
```

They are not part of this repo.

### Layout

This pack follows the ScreenFlow project model (screen features / originals / match setups):

```text
.
├── project.json              # Runtime, page list, vars, etc.
├── pages/{page_id}/
│   ├── page.json             # Features, originals, match setups, recognition, case tree, actions, post-listen
│   ├── sources/              # Page originals (full-window screenshots; Studio material)
│   └── features/             # Derived match crops (runtime templates)
└── README.md                 # This file (Chinese + English)
```

Pages roughly cover: main, character maintenance, forge, melt confirm, rewards, hero select, in-game, and results.

For engine concepts (case trees, post-listen, script steps, Web Studio), see the [ScreenFlow README](https://github.com/No404error/screenflow-studio).

### Disclaimer

For learning and technical exchange only. Automation may violate game or platform terms and can risk account action. **You assume all risk.** Authors are not liable for any loss. Use only where lawful and permitted.

### Links

- Engine / Studio: [screenflow-studio](https://github.com/No404error/screenflow-studio)
