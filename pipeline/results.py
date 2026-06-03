# results.py — 2026 Alameda 12u All-Stars
# Complete game results log.
# Fields: date, away, home, away_score, home_score, winner, field, round
#
# round options: "Districts", "Sections", "State", "Scrimmage"
# field: name of the field/complex where the game was played
# All dates must be YYYY-MM-DD format

GAMES = [
    # ── Scrimmages ─────────────────────────────────────────────────────────
    {"date": "2026-06-03", "away": "Alameda", "home": "Crabs 12U",
     "away_score": 20, "home_score": 8, "winner": "Alameda",
     "field": "TBD", "round": "Scrimmage"},

    # ── Districts ──────────────────────────────────────────────────────────
    # {"date": "2026-07-XX", "away": "Alameda", "home": "Opponent",
    #  "away_score": 0, "home_score": 0, "winner": "Alameda",
    #  "field": "TBD", "round": "Districts"},

    # ── Sections ───────────────────────────────────────────────────────────
    # {"date": "2026-07-XX", "away": "Alameda", "home": "Opponent",
    #  "away_score": 0, "home_score": 0, "winner": "Alameda",
    #  "field": "TBD", "round": "Sections"},

    # ── State ──────────────────────────────────────────────────────────────
    # {"date": "2026-08-XX", "away": "Alameda", "home": "Opponent",
    #  "away_score": 0, "home_score": 0, "winner": "Alameda",
    #  "field": "TBD", "round": "State"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "Alameda")
    losses = sum(1 for g in GAMES if g["winner"] != "Alameda")
    return wins, losses


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "Alameda" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "Alameda" else g["away_score"] for g in GAMES)
    return scored, allowed
