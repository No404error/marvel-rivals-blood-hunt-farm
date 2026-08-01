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
| 符文觉醒 | **Rune Awakening** | Right-side Ability Trait branch for Thor in Blood Hunt (vs left **Thunder Formation** / Storm Surge) |
| 觉醒符文 | **Awakening Rune** | The awakening state / ability uptime this build relies on |
| 不灭符文 | **Immortal Rune** | Trait that extends **Awakening Rune duration** (critical for long AFK uptime) |

Difficulty ladder in Blood Hunt (official English): **Normal → Hard → Extreme → Nightmare**.  
Community nicknames for this setup: **Lightning Aura Thor** / **Awakening Thor** (AFK aura clear).

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
| Party | **Solo preferred**—do not party up or fill teammates; the script is tuned for a single-player flow |
| Note | Other modes or Nightmare floors are **not** supported |

#### Hero / build (strongly recommended)

| Item | Requirement |
|------|-------------|
| Hero | **Thor** |
| Build path | **Rune Awakening** (right Ability Trait tree)—not the left **Thunder Formation** / Storm Surge path |
| Duration | **Long Awakening Rune uptime** (prioritize traits like **Immortal Rune** that add Awakening Rune duration) so F/awakening covers full waves |
| Damage | **High enough** to clear vampire waves under F / awakening AFK pacing (often called a **Lightning Aura** setup) |
| Health / survivability | **High enough** so you are not downed by trash mobs |
| Note | The script does **not** move, heal, or use other abilities. Short awakening, low damage, or a Storm Surge active build will fail or stall. |

#### Runtime

| Item | Requirement |
|------|-------------|
| OS | Windows |
| Python | 3.10+ recommended |
| Privileges | **Must** run as Administrator (the exe requests UAC elevation; otherwise input will not reach the game) |
| Window | Game **in foreground**, not occluded |
| Resolution | Reference **2559×1439** (~1440p); scaling is attempted, but large mismatches need new templates |
| Client language | Templates target the **Simplified Chinese** UI unless you replace them |
| Dependencies | See `requirements.txt` |

---

### Install & run

```powershell
cd E:\mr
pip install -r requirements.txt

# Required: open PowerShell / terminal as Administrator
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

---

### Build a Windows exe

Everything (including `templates/`) is **embedded in one exe**.

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1 -Version 1.0.0
```

Outputs:

| Path | Description |
|------|-------------|
| `dist\auto_farm.exe` | Single-file app (templates inside) |
| `dist\marvel-rivals-blood-hunt-farm-v1.0.0-win64.zip` | Zip for GitHub Releases |

Run `auto_farm.exe` (UAC admin elevation is required)—no separate `templates` folder.

---

### Publish a GitHub Release

```powershell
git tag v1.0.0
git push origin v1.0.0

gh release create v1.0.0 `
  .\dist\marvel-rivals-blood-hunt-farm-v1.0.0-win64.zip `
  --title "v1.0.0" `
  --notes-file RELEASE_NOTES.md
```

Or: repo → **Releases** → **Draft a new release** → tag `v1.0.0` → upload the zip → Publish.
