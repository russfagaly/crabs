# results.py — 2026 North Oakland LL (NOLL) 12U All-Stars
# Game results log. Fields: date, away, home, away_score, home_score, winner, field, round
# round options: "Scrimmage", "Districts", "Sections", "State". Dates: YYYY-MM-DD.
# NOLL is recorded as the "away" team in every entry (home = opponent).

GAMES = [
    # ── Scrimmages ─────────────────────────────────────────────────────────
    {"date": "2026-06-07", "away": "NOLL", "home": "TBD",
     "away_score": 16, "home_score": 2, "winner": "NOLL",
     "field": "TBD", "round": "Scrimmage"},

    # ── Districts ──────────────────────────────────────────────────────────
    {"date": "2026-06-20", "away": "NOLL", "home": "Concord American LL 2026 All-Stars",
     "away_score": 8, "home_score": 1, "winner": "NOLL",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-24", "away": "NOLL", "home": "Martinez 12U All-Stars",
     "away_score": 1, "home_score": 3, "winner": "Martinez 12U All-Stars",
     "field": "TBD", "round": "Districts"},
    {"date": "2026-06-27", "away": "NOLL", "home": "WCLL 12U All-Stars",
     "away_score": 6, "home_score": 5, "winner": "NOLL",
     "field": "TBD", "round": "Districts"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "NOLL")
    losses = sum(1 for g in GAMES if g["winner"] != "NOLL")
    return wins, losses


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "NOLL" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "NOLL" else g["away_score"] for g in GAMES)
    return scored, allowed
