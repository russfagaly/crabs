# results.py — Lafayette Lightning

GAMES = [
    # ── Cooperstown ──────────────────────────────────────────────────────────
    # G1 — Lightning away (batted top)
    {"date": "2026-06-06", "away": "Lafayette", "home": "GRIT Gulf Coast",
     "away_score": 12, "home_score": 18, "winner": "GRIT Gulf Coast",
     "field": "Field TBD", "round": "Cooperstown"},
    # G2 — Lightning home (batted bottom)
    {"date": "2026-06-06", "away": "ZT Prospects 12U", "home": "Lafayette",
     "away_score": 14, "home_score": 2, "winner": "ZT Prospects 12U",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/07 G1 — Lightning home (batted bottom); ended in a tie
    {"date": "2026-06-07", "away": "BCB De Jesus 12U", "home": "Lafayette",
     "away_score": 11, "home_score": 11, "winner": "Tie",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/07 G2 — Lightning away (batted top); walk-off loss
    {"date": "2026-06-07", "away": "Lafayette", "home": "Oconee Riverdawgs 12U",
     "away_score": 5, "home_score": 6, "winner": "Oconee Riverdawgs 12U",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/08 G1 — Lightning away (batted top); run-rule win
    {"date": "2026-06-08", "away": "Lafayette", "home": "USA Prime Midwest 12U",
     "away_score": 14, "home_score": 3, "winner": "Lafayette",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/08 G2 — Lightning home (batted bottom); ended in a tie
    {"date": "2026-06-08", "away": "LMB Cooperstown 12U", "home": "Lafayette",
     "away_score": 11, "home_score": 11, "winner": "Tie",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/09 G1 — Lightning home (batted bottom); comeback win
    {"date": "2026-06-09", "away": "TX Action Baseball Cooperstown 12U", "home": "Lafayette",
     "away_score": 8, "home_score": 13, "winner": "Lafayette",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/09 G2 — Lightning home (batted bottom); walk-off win
    {"date": "2026-06-09", "away": "Central Iowa Showtime 12U", "home": "Lafayette",
     "away_score": 8, "home_score": 9, "winner": "Lafayette",
     "field": "Field TBD", "round": "Cooperstown"},
    # 06/10 — Lightning away (batted top); run-rule loss (Oconee rematch)
    {"date": "2026-06-10", "away": "Lafayette", "home": "Oconee Riverdawgs 12U",
     "away_score": 8, "home_score": 17, "winner": "Oconee Riverdawgs 12U",
     "field": "Field TBD", "round": "Cooperstown"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "Lafayette")
    ties   = sum(1 for g in GAMES if g["winner"] == "Tie")
    losses = len(GAMES) - wins - ties
    return wins, losses, ties


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "Lafayette" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "Lafayette" else g["away_score"] for g in GAMES)
    return scored, allowed
