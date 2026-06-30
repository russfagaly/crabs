# results.py — 2026 Alameda 12u All-Stars
# Complete game results log.
# Fields: date, away, home, away_score, home_score, winner, field, round
#
# round options: "Districts", "Sections", "State", "Scrimmage"
# field: name of the field/complex where the game was played
# All dates must be YYYY-MM-DD format

GAMES = [
    # Alameda Crabs — District tournament games
    {"date": "2026-06-20", "away": "Alameda", "home": "Pinole Hercules",
     "away_score": 29, "home_score": 8, "winner": "Alameda",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-24", "away": "Alameda", "home": "SOLL 12U All-Stars",
     "away_score": 9, "home_score": 10, "winner": "SOLL 12U All-Stars",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-27", "away": "Alameda", "home": "LLL 12u All-Stars",
     "away_score": 6, "home_score": 0, "winner": "Alameda",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-29", "away": "Alameda", "home": "NOLL 12U All-Stars",
     "away_score": 7, "home_score": 2, "winner": "Alameda",
     "field": "TBD", "round": "Districts"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "Alameda")
    losses = sum(1 for g in GAMES if g["winner"] != "Alameda")
    return wins, losses


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "Alameda" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "Alameda" else g["away_score"] for g in GAMES)
    return scored, allowed
