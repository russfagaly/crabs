# results.py — 2026 North Oakland LL (SOLL) 12U All-Stars
# Game results log. Fields: date, away, home, away_score, home_score, winner, field, round
# round options: "Scrimmage", "Districts", "Sections", "State". Dates: YYYY-MM-DD.
# SOLL is recorded as the "away" team in every entry (home = opponent).

GAMES = [
    # South Oakland LL (SOLL) 12U All-Stars
    {"date": "2026-06-19", "away": "SOLL", "home": "LLL 12u All-Stars",
     "away_score": 9, "home_score": 4, "winner": "SOLL",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-20", "away": "SOLL", "home": "WCLL 12u All-Stars",
     "away_score": 8, "home_score": 7, "winner": "SOLL",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-24", "away": "SOLL", "home": "Alameda Crabs",
     "away_score": 10, "home_score": 9, "winner": "SOLL",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-27", "away": "SOLL", "home": "Martinez 12U All-Stars",
     "away_score": 1, "home_score": 2, "winner": "Martinez 12U All-Stars",
     "field": "TBD", "round": "Districts"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "SOLL")
    losses = sum(1 for g in GAMES if g["winner"] != "SOLL")
    return wins, losses


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "SOLL" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "SOLL" else g["away_score"] for g in GAMES)
    return scored, allowed
