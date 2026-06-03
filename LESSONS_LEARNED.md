# Lessons Learned — 2026 Alameda Majors Season
## Applied to the 12u All-Stars Pipeline

This document captures every bug, gotcha, and hard-won lesson from the 166-game 2026 regular season.

---

## Data Entry

### Date Format — Always YYYY-MM-DD
**Problem:** Early game files used `03/07` format for dates. The pipeline sorts games lexicographically, so `03/07` and `04/15` sort correctly by accident — until you have `12/01` which sorts before `02/01`. YYYY-MM-DD eliminates this entirely.
**Rule:** Always use `DATE = "2026-07-04"` format. Never `"07/04"`.

### Innings Pitched Thirds
**Problem:** `3.3` IP is mathematically 3.3 but logically means 3 full innings + 3 outs = 4.0 innings. The `.3` notation should never appear.
**Rule:** IP can only end in `.0`, `.1`, or `.2`. If someone throws a complete inning after `.2`, it becomes the next whole number.

### Doubles + Triples + HR Must Not Exceed Hits
**Problem:** Transcription errors sometimes had `doubles=2` when the player only had `h=1`.
**Rule:** `doubles + triples + hr ≤ h` always. The checklist in the game template catches this.

### Batters Faced Verification
**Problem:** `bf` was sometimes entered incorrectly from scoresheets.
**Rule:** BF = AB + BB + HBP for a given pitcher. Cross-check against the hitting side.

---

## Name Management

### GameChanger Truncates Long Names
**Problem:** GameChanger's app truncates first names longer than ~7 characters. "Sebastian" becomes "Sebasti...", "Benjamin" becomes "Benjami...".
**Solution:** Register the truncated form in `name_registry.py`. Use the truncated form in game files too. The validator will catch inconsistencies.

### Nicknames vs. Legal Names
**Problem:** Players who go by nicknames cause mismatches if different scorekeepers use different names.
**Solution:** Document all known nickname mappings in `name_registry.py` comments. Enforce the nickname form consistently. From the 2026 season:
- Wallace Beaver → "Ace B" (goes by Ace)
- John Griswold → "Jack G" (goes by Jack)
- Robert Fagaly → "RJ F" (goes by RJ)
- Andrew Bryant → "Drew B" (goes by Drew)

### Hyphenated Last Names
**Problem:** GameChanger abbreviates hyphenated names to just the first letter (Jordan Cerda-Zein → "Jordan C").
**Solution:** Register as the abbreviated form. The player's full name lives in `roster.py`.

---

## Pipeline Architecture

### Validate Before Every Compile
**Problem:** Running `compile.py` with a bad game file produces silent errors or wrong totals.
**Rule:** Always run `validate.py` first. Better: use `recompile.sh` which runs validate → compile → sheets and aborts if validation fails.

### Google Sheets vs. Excel
The pipeline maintains both:
- `compile.py` → local `.xlsx` file (fast, works offline)
- `compile_sheets.py` → Google Sheets (accessible anywhere, shareable)

For the all-star season, decide early which one is "the source of truth" and stick to it.

### The All-Star Tracker Tab
The regular season spreadsheet had an All-Star Tracker tab that showed L5 (last 5 games) and post-break stats for a defined roster subset. For the all-star season, consider building a simpler equivalent:
- Season totals
- Last 3 games (smaller sample since there are fewer games total)
- Pitch count summary

---

## Stats Insights from the Regular Season

### OPS vs. OPS+
OPS is absolute; OPS+ benchmarks against the league average (100 = average, 150 = 50% above). For the all-star season, you won't have a "league average" from opponents — so OPS+ would need to be benchmarked against your own team, or dropped.

### opWAR
The offensive + pitching WAR metric developed during this season works well for comparing players but requires a meaningful run environment to calibrate. For a short tournament season (5–10 games), the sample size is too small for reliable WAR. OPS and ERA are more meaningful with limited data.

### L5 Stats
The "last 5 games" window was very useful for identifying hot/cold players during the regular season. For an all-star tournament, "last 2 games" or "last 3 games" is the equivalent — adjust the window based on how many games you play.

### BAA (Batting Average Against)
One of the most useful pitching stats. Unlike ERA, it isn't affected by unearned runs or fielding. Tracks how hard batters are hitting the pitcher directly. Formula: `H / (BF - BB - HBP)`.

---

## Tournament-Specific Considerations

### Opponent Stats
The regular season tracked both teams' stats. For all-stars, opponent stats are optional — you don't have their rosters. However, tracking opponent totals (runs, hits, errors) is useful for tournament summaries.

### One Team, Many Opponents
The regular season pipeline was designed for 8 teams. For all-stars, simplify `TEAM = "Alameda"` and only create game files for Alameda players. The compile script will need a small adjustment to not expect opponent game files.

### Pitch Count Is Now Mission-Critical
In the regular season, pitch counts were interesting stats. In tournament play, they're compliance requirements. Build in a daily check before each game to confirm eligibility.

### Momentum Tracking
Tournament teams often have 1–2 day gaps between games. The L5 tracker equivalent is very useful here for identifying who's locked in vs. who needs at-bats.

---

*Prepared June 2026 — End of 2026 Alameda Majors regular season.*
*Total games tracked: 166 | Players tracked: 96 | Teams: 8*
