# Marvel Rivals · Blood Hunt Auto-Farm

**Language / 语言:** [中文](README.md) | [English](README.en.md)

---

> Localization note: Proper nouns follow **Marvel Rivals** English client / official patch & community usage.  
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
