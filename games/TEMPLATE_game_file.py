"""
2026 Alameda 12u All-Stars
Opponent: [Opponent Name]
Date:     MM/DD
Round:    Districts / Sections / State / Scrimmage
Result:   W/L  Score: X-X
Field:    [Field Name]
"""

# ⚠️  DATE must be YYYY-MM-DD format (not MM/DD) — pipeline sorts by date string
TEAM = "Alameda"
DATE = "2026-MM-DD"   # ← change this

# ── HITTING ───────────────────────────────────────────────────────────────────
# One dict per player. Include every player in the lineup, even 0-for-0.
# Name format: "FirstInitial LastName #Jersey"  e.g.  "Adrien R #6"
# All fields required — use 0 for any stat that didn't happen.

hitting = [
    # {"name": "First L #N", "ab": 0, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0,
    #  "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0},
]

# ── PITCHING ──────────────────────────────────────────────────────────────────
# One dict per pitcher appearance, in order pitched.
# ip format: "3.0" = 3 full innings, "2.1" = 2⅓ innings, "0.2" = ⅔ inning
# ⚠️  Never use .3 — e.g. "3.3" is wrong, use "4.0" instead

pitching = [
    # {"name": "First L #N", "ip": "0.0", "h": 0, "r": 0, "er": 0, "bb": 0, "so": 0,
    #  "pitches": 0, "strikes": 0, "bf": 0, "hbp": 0, "hr": 0},
]

# ── CHECKLIST (delete before saving) ─────────────────────────────────────────
# [ ] DATE is YYYY-MM-DD format
# [ ] All lineup players are in hitting list
# [ ] All pitchers are in pitching list
# [ ] Doubles + triples + hr ≤ h for every hitter
# [ ] hr (home runs allowed) set for each pitcher — used for FIP
# [ ] IP uses correct thirds notation (.0, .1, .2 only — never .3)
# [ ] Team hit total matches sum of individual h values
# [ ] Results.py updated with this game's score
# [ ] Run: python3 pipeline/validate.py  (must show ✅ No errors)
