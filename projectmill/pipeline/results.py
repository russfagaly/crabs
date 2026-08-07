# results.py — Project Mill Cooperstown 12U
# Cooperstown All Star Village, August 2026.
#
# IMPORTANT: same-date games are matched to game files by filename sort order,
# so the order here must match the G1/G2 order in games/. Both 08-05 games are
# listed in the order they were played (CK Cardinals first, then Morrisville).

GAMES = [
    # ── Cooperstown ──────────────────────────────────────────────────────────
    # 08/05 G1 — Project Mill away (batted top); lost the lead in the bottom 5th
    {"date": "2026-08-05", "away": "Project Mill", "home": "CK Cardinals 12U Red",
     "away_score": 2, "home_score": 3, "winner": "CK Cardinals 12U Red",
     "field": "Cooperstown All Star Village", "round": "Cooperstown"},
    # 08/05 G2 — Project Mill home (batted bottom); six-run 3rd broke it open
    {"date": "2026-08-05", "away": "Morrisville Riverdogs 12U", "home": "Project Mill",
     "away_score": 13, "home_score": 2, "winner": "Morrisville Riverdogs 12U",
     "field": "Cooperstown All Star Village", "round": "Cooperstown"},
    # 08/06 G1 — Project Mill home (batted bottom)
    {"date": "2026-08-06", "away": "Lake Washington 12U", "home": "Project Mill",
     "away_score": 14, "home_score": 3, "winner": "Lake Washington 12U",
     "field": "Cooperstown All Star Village", "round": "Cooperstown"},
    # 08/06 G2 — Project Mill away (batted top); led 10-8, lost on a walk-off
    {"date": "2026-08-06", "away": "Project Mill", "home": "Canes Triad Gold 12U",
     "away_score": 10, "home_score": 11, "winner": "Canes Triad Gold 12U",
     "field": "Cooperstown All Star Village", "round": "Cooperstown"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "Project Mill")
    ties   = sum(1 for g in GAMES if g["winner"] == "Tie")
    losses = len(GAMES) - wins - ties
    return wins, losses, ties


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "Project Mill" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "Project Mill" else g["away_score"] for g in GAMES)
    return scored, allowed
