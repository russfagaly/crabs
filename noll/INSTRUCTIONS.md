# 2026 Alameda Little League — 12u All-Stars Stats Pipeline
## Setup & Operations Guide

---

## Overview

This pipeline tracks individual player hitting and pitching stats for the 2026 Alameda 12u All-Star season. It ingests per-game data files, validates them, compiles a master Excel workbook, and optionally pushes to a Google Sheet.

The system was developed and battle-tested across a full 166-game Alameda Majors regular season. This guide captures everything learned along the way.

---

## Folder Structure

```
2026_12u_AllStars/
├── INSTRUCTIONS.md          ← this file
├── games/                   ← one .py file per game
│   └── 2026_07_04_Opponent.py
├── pipeline/
│   ├── compile.py           ← builds the Excel workbook
│   ├── compile_sheets.py    ← pushes to Google Sheets (optional)
│   ├── validate.py          ← validates game files before compile
│   ├── roster.py            ← player roster and metadata
│   ├── name_registry.py     ← maps jersey numbers to name strings
│   ├── results.py           ← game results log
│   └── recompile.sh         ← one-command full pipeline run
└── 2026 12u AllStars Stats.xlsx   ← compiled output (auto-generated)
```

---

## Game File Format

Each game gets its own Python file in the `games/` folder.

**Naming convention:** `YYYY_MM_DD_OpponentName.py`

Example: `2026_07_04_San Ramon.py`

⚠️ **Critical:** The date must be in `YYYY-MM-DD` format inside the file (not MM/DD). The pipeline sorts games chronologically using string comparison, so `2026-07-04` works — `07/04` does not.

### Game File Template

```python
"""
2026 Alameda 12u All-Stars
Opponent: San Ramon
Date:     07/04
"""
TEAM = "Alameda"
DATE = "2026-07-04"

hitting = [
    # name format: "FirstInitial LastName #Jersey"
    # Example: "Adrien R #6"
    {"name": "Player A #1",  "ab": 3, "r": 1, "h": 2, "rbi": 1, "bb": 0, "so": 1,
     "doubles": 1, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0},
]

pitching = [
    {"name": "Player A #1",  "ip": "3.0", "h": 2, "r": 1, "er": 1, "bb": 1, "so": 4,
     "pitches": 42, "strikes": 28, "bf": 11, "hbp": 0},
]
```

### Hitting Fields

| Field | Description |
|-------|-------------|
| `ab` | At bats |
| `r` | Runs scored |
| `h` | Total hits |
| `rbi` | Runs batted in |
| `bb` | Walks |
| `so` | Strikeouts |
| `doubles` | Two-base hits |
| `triples` | Three-base hits |
| `hr` | Home runs |
| `sb` | Stolen bases |
| `cs` | Caught stealing |
| `e` | Errors committed |
| `hbp` | Hit by pitch |

### Pitching Fields

| Field | Description |
|-------|-------------|
| `ip` | Innings pitched as string: `"3.0"`, `"2.1"`, `"0.2"` |
| `h` | Hits allowed |
| `r` | Runs allowed (earned + unearned) |
| `er` | Earned runs allowed |
| `bb` | Walks |
| `so` | Strikeouts |
| `pitches` | Total pitches thrown |
| `strikes` | Strikes thrown |
| `bf` | Batters faced |
| `hbp` | Hit batters |

**IP format:** Uses baseball thirds notation. `3.1` = 3 and 1/3 innings. `3.2` = 3 and 2/3 innings. Never use `.3` — that would be a full inning, write it as the next whole number.

---

## Player Names — The Most Important Rule

The `name` field in game files must **exactly match** the format expected by `name_registry.py`. The pipeline uses a `display_name()` function that truncates names to `"FirstI LastName"` format (e.g. `"Adrien R"`).

### Lessons Learned from the Regular Season

1. **GameChanger truncates long names.** If a player's name is long (e.g. "Sebastian" or "Benjamin"), GameChanger's app will show it as "Sebasti..." or "Benjami...". Use the truncated version in game files and register it in `name_registry.py` exactly as it appears.

2. **Nicknames vs. legal names.** Some players go by nicknames. Document these in `name_registry.py`. Examples from the regular season:
   - Wallace Beaver → goes by "Ace" → game files use `"Ace B #44"`
   - John Griswold → goes by "Jack" → game files use `"Jack G #27"`

3. **Validation will catch mismatches.** Run `python3 pipeline/validate.py` before every compile. It will flag any name in a game file that doesn't match the registry.

4. **Jersey numbers change.** If a player changes jersey numbers, update `name_registry.py`. The registry maps `(team, jersey_number)` → name string.

---

## Running the Pipeline

### Quick compile (Excel only)
```bash
cd /path/to/2026_12u_AllStars
python3 pipeline/validate.py && python3 pipeline/compile.py
```

### Full pipeline (validate → Excel → Google Sheets)
```bash
bash pipeline/recompile.sh
```

### Individual steps
```bash
python3 pipeline/validate.py      # check game files for errors
python3 pipeline/compile.py       # build Excel workbook
python3 pipeline/compile_sheets.py  # push to Google Sheets
```

---

## results.py Format

Every game result goes in `results.py`. This powers the Standings & Results tab.

```python
GAMES = [
    # ── Districts ──────────────────────────────────────────────────────────
    {"date": "2026-07-04", "away": "Alameda", "home": "San Ramon",
     "away_score": 8, "home_score": 3, "winner": "Alameda", "field": "Wally Pond"},
]
```

**Fields:** `date` (YYYY-MM-DD), `away`, `home`, `away_score`, `home_score`, `winner`, `field`

---

## Computed Stats Reference

The pipeline auto-computes the following from raw game data:

### Hitting
- **AVG** = H / AB
- **OBP** = (H + BB + HBP) / (AB + BB + HBP + SF)
- **SLG** = Total Bases / AB
- **OPS** = OBP + SLG
- **OPS+** = 100 × (OBP/lgOBP + SLG/lgSLG − 1)
- **ISO** = SLG − AVG
- **TB** = 1B + 2×2B + 3×3B + 4×HR

### Pitching
- **ERA** = (ER × 9) / IP
- **WHIP** = (H + BB) / IP
- **K/IP** = SO / IP
- **BAA** = H / (BF − BB − HBP)  ← batting average against
- **Strike%** = Strikes / Pitches
- **FIP** = (13×HR + 3×(BB+HBP) − 2×K) / IP + FIP_constant

---

## Setting Up Google Sheets (Optional)

1. Create a Google Cloud project and enable the Sheets API
2. Download `credentials.json` and place in `pipeline/`
3. Install dependencies: `pip install gspread google-auth`
4. On first run, `compile_sheets.py` will prompt for OAuth authorization
5. The sheet ID is configured at the top of `compile_sheets.py`

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Validation error: name not in registry | Game file uses a different name format | Update `name_registry.py` or fix the name in the game file |
| Wrong chronological order | Date in game file is MM/DD instead of YYYY-MM-DD | Change to YYYY-MM-DD format |
| IP arithmetic wrong | Used `.3` instead of next whole number | `3.3` should be `4.0` |
| Stats don't add up | Forgot to include a player in hitting list | Check game scoresheet against file |
| OBP seems off | SF (sacrifice flies) not tracked in game files | SF is pulled from GameChanger event files via `event_stats.py` |

---

## All-Star Season Notes

A few differences from the regular season to keep in mind:

- **One team only.** Unlike the regular season where both teams' stats are tracked, for all-stars you only need to track Alameda players. You can skip creating opponent game files unless you want opponent stats.
- **Tournament format.** Games are elimination rounds — label clearly in `results.py` (Districts, Sections, State, etc.)
- **Pitch count limits.** Little League has strict pitch count and rest rules for tournament play. Consider adding a `pitch_count_tracker.py` to monitor cumulative pitch counts and required rest days.
- **Different fields.** Keep the `field` field accurate in `results.py` for travel/logistics reference.
- **Larger player pool.** All-star rosters are typically 13 players. Some tournaments allow a larger travel roster.

---

## Pitch Count Tracking (Tournament Critical)

Little League pitch count rules for 12u:
- **1–20 pitches:** No rest required
- **21–35 pitches:** 1 calendar day rest
- **36–50 pitches:** 2 calendar days rest
- **51–65 pitches:** 3 calendar days rest
- **66+ pitches:** 4 calendar days rest

The `pitches` field in each pitching row enables automatic pitch count monitoring. Consider building a simple summary script that shows each pitcher's cumulative pitches and next available date.

---

*Guide prepared June 2026. Based on the 2026 Alameda Little League Majors season (166 games, 96 players).*
