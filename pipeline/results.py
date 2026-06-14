# results.py — 2026 Alameda 12u All-Stars
# Complete game results log.
# Fields: date, away, home, away_score, home_score, winner, field, round
#
# round options: "Districts", "Sections", "State", "Scrimmage"
# field: name of the field/complex where the game was played
# All dates must be YYYY-MM-DD format

GAMES = [
    # ── Scrimmages ─────────────────────────────────────────────────────────
    {"date": "2026-06-02", "away": "Alameda", "home": "Palo Alto LL 12U",
     "away_score": 20, "home_score": 8, "winner": "Alameda",
     "field": "TBD", "round": "Scrimmage"},
    {"date": "2026-06-04", "away": "Alameda", "home": "Danville LL 12U",
     "away_score": 3, "home_score": 4, "winner": "Danville LL 12U",
     "field": "Danville", "round": "Scrimmage"},
    {"date": "2026-06-06", "away": "Alameda", "home": "San Ramon Valley LL 12U",
     "away_score": 3, "home_score": 8, "winner": "San Ramon Valley LL 12U",
     "field": "TBD", "round": "Scrimmage"},
    {"date": "2026-06-06", "away": "Alameda", "home": "San Ramon Valley LL 12U",
     "away_score": 6, "home_score": 16, "winner": "San Ramon Valley LL 12U",
     "field": "TBD", "round": "Scrimmage"},
    {"date": "2026-06-09", "away": "Alameda", "home": "Castro Valley LL 12U",
     "away_score": 10, "home_score": 3, "winner": "Alameda",
     "field": "TBD", "round": "Scrimmage"},
    {"date": "2026-06-11", "away": "Alameda", "home": "San Mateo",
     "away_score": 2, "home_score": 12, "winner": "San Mateo",
     "field": "TBD", "round": "Scrimmage"},
    {"date": "2026-06-13", "away": "Alameda", "home": "San Francisco LL 12U",
     "away_score": 24, "home_score": 1, "winner": "Alameda",
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
