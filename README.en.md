# Marvel Rivals · Blood Hunt Auto-Farm

**Language / 语言:** [中文](README.md) | [English](README.en.md)

This repository is a **[ScreenFlow](https://github.com/No404error/screenflow-studio)** **project pack**: foreground capture + template matching to loop Blood Hunt — start a run, clear gear when full, pick a hero, press F in combat, and return from the results screen.

It contains **only project config and image assets**. The engine is not included. Run it with ScreenFlow Studio.

---

## Important: assets are for Simplified Chinese UI

Everything under `pages/` (detect images, click images, and text-dependent matches) was captured from the **Simplified Chinese** client.

- If you use the **English** (or any other language) client, **do not expect these assets to work as-is**.  
- Use the farm logic below as a guide, then **reconfigure pages, states (state trees), and detect/click images yourself** in Studio before running.  
- Resolution changes or UI patches also require recapturing templates or adjusting the project reference resolution.

---

## What it does (farm logic)

With the game in the foreground, the intended loop is:

1. On the main screen, click Start  
2. If gear is full: Character Maintenance → Forge → select all → melt → confirm rewards → back to main  
3. Hero select: if Thor is already shown, confirm; otherwise pick Thor then confirm  
4. In match: press **F** only when the bottom-right F prompt is “ready”  
5. Results: skip → back to main → start again  

No memory reading, no injection. Background (non-foreground) play is not supported.

---

## How to use

### 1. Install ScreenFlow

Get Studio from the engine repo:

- Repository: [No404error/screenflow-studio](https://github.com/No404error/screenflow-studio)  
- From source: `python .\run_studio.py`  
- Or launch `ScreenFlow.exe` from a release build

### 2. Open this project

In Studio: **File → Open Project Folder…**, select **this repository root** (the folder that contains `project.json` and `pages/`).

### 3. Game setup

| Item | Requirement |
|------|-------------|
| Mode | Manually select **Blood Hunt** on the main screen (this pack does not switch modes) |
| Difficulty | Prefer **Nightmare 1** |
| Party | Prefer **solo** |
| Resolution | Templates were taken around **2560×1440**; other resolutions may need new crops or a different reference size |
| Client language | Bundled assets = **Simplified Chinese**; other languages → reconfigure pages / states / images |
| Foreground | Keep the game focused while the engine runs |

### 4. Run

1. Match assets to your client language (rebuild the pack if not Chinese)  
2. Tweak run settings in Studio if needed, then **Save**  
3. Click **Start** (Windows may show UAC once for the elevated engine process)  
4. Use Pause / Continue / Stop as needed  

---

## Layout

```text
.
├── project.json          # Runtime, page list, look-alike pairs
├── pages/{page_id}/
│   ├── page.json         # Detection + state tree + actions
│   ├── detect/           # Detect images (Simplified Chinese UI)
│   └── click/            # Click targets (Simplified Chinese UI)
├── README.md             # Chinese
└── README.en.md          # English
```

Studio UI preferences (language, recent projects, etc.) live under the user profile (e.g. `%USERPROFILE%\.screenflow\ui.json`), not in this repo.

---

## Disclaimer

For learning and technical exchange only. Automation may violate game or platform terms and can risk account action. **You assume all risk.** Authors are not liable for any loss. Use only where lawful and permitted.

---

## Links

- Engine / Studio: [screenflow-studio](https://github.com/No404error/screenflow-studio)
