# Marvel Rivals · Blood Hunt Auto-Farm

**Language / 语言:** [中文](README.md) | [English](README.en.md)

> Templates were captured from the **Simplified Chinese** client. English UI will not match unless you replace templates.

---

### Disclaimer

1. This tool is for **learning and technical research only** (screen matching + input simulation).
2. Automation may **violate Marvel Rivals / platform Terms of Service** and risk warnings, restrictions, or bans. **You assume all responsibility.**
3. Authors are **not liable** for any loss (account, progress, device, etc.).
4. Do not use commercially or to undermine fair play.
5. Game updates may break the tool; keep an eye on releases and notes.
6. **By using this tool, you agree to the above.**

---

### What it does

With the game in the **foreground** and the app running as **Administrator**, it loops:

1. Lobby: click **Start**
2. Hero select: **Confirm** if **Thor** is selected; otherwise select Thor then Confirm; if **Cancel** is shown, wait
3. In match: press **F** only when that ability is **Ready**
4. Results: long-press **Space** to skip → **Esc** back to lobby → next run

Not memory reading, not injection, and not true background AFK.

---

### Requirements before use

| Item | Requirement |
|------|-------------|
| Mode | Manually select **Blood Hunt** on the lobby (the tool does not switch modes) |
| Difficulty | **Nightmare 1** |
| Party | **Solo preferred** (no party / fill teammates) |
| Hero | **Thor**, **Rune Awakening** build (right trait tree; not Thunder Formation / Storm Surge) |
| Duration | **Long Awakening Rune uptime** (e.g. prioritize **Immortal Rune**) so AFK covers waves |
| Damage / survivability | **High enough**—the tool does not move or heal |
| OS | Windows |
| Privileges | **Administrator required**; the app requests elevation via UAC at startup (click Yes) |
| Window | Game focused and not occluded |
| Resolution | Around **2560×1440** (reference 2559×1439) |
| Client language | Templates target **Simplified Chinese** UI |

**Glossary (short):** 血猎 → Blood Hunt · 符文觉醒 → Rune Awakening · 觉醒符文 → Awakening Rune · 不灭符文 → Immortal Rune · 开始游戏 → Start · 确定/取消 → Confirm/Cancel

---

### Download & use (recommended)

1. Open this repo’s **[Releases](../../releases)** page  
2. Download the latest zip (e.g. `marvel-rivals-blood-hunt-farm-v*.zip`) and extract it  
3. Run **`auto_farm.exe`**—it will request Administrator rights at startup; click Yes on UAC  
4. Focus the game window; after elevation, automation starts in about 3 seconds  

Hotkeys:

| Key | Action |
|-----|--------|
| F9 | Start / resume |
| F10 | Pause |
| F11 | Quit |

---

### Run from source (optional)

```powershell
pip install -r requirements.txt
# Required: terminal opened as Administrator
python .\auto_farm.py
```

---

### Limitations

- The game must stay in the foreground.
- UI / costume / language / resolution changes can break recognition.
- Only the **F Ready** state is handled in combat—**clearing is not guaranteed**.
- Account and ToS risk is yours alone.
