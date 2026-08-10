# results.py — Road Dogs 12 (GameChanger: "Barkers aka Road Dogs 12U")
# Mixed tournament play, summer 2026.
#
# "round" is a free-text display label. Set it per game to the actual tournament
# name once known; "Tournament" is a neutral placeholder.
#
# IMPORTANT: same-date games are matched to game files by filename sort order,
# so the order here must match the G1/G2 order in games/.

GAMES = [
    # 06/13 G1 — Road Dogs away (batted top)
    {"date": "2026-06-13", "away": "Road Dogs", "home": "Delta Valley Bruins 12U",
     "away_score": 13, "home_score": 10, "winner": "Road Dogs",
     "field": "TBD", "round": "Tournament"},
    # 06/13 G2 — Road Dogs away (batted top); lost on a walk-off in the 6th
    {"date": "2026-06-13", "away": "Road Dogs", "home": "East Bay Gamers BATS",
     "away_score": 5, "home_score": 6, "winner": "East Bay Gamers BATS",
     "field": "TBD", "round": "Tournament"},
    # 06/14 — Road Dogs home (batted bottom); Oliver R home run
    {"date": "2026-06-14", "away": "Delta Valley Bruins 12U", "home": "Road Dogs",
     "away_score": 10, "home_score": 7, "winner": "Delta Valley Bruins 12U",
     "field": "TBD", "round": "Tournament"},
    # 06/15 — Road Dogs away (batted top); 7-inning game, six 1-inning pitchers
    {"date": "2026-06-15", "away": "Road Dogs", "home": "Alameda All-Stars 11U",
     "away_score": 2, "home_score": 7, "winner": "Alameda All-Stars 11U",
     "field": "TBD", "round": "Tournament"},
    # 07/16 — Road Dogs away (batted top); out-hit WCLL 10-7 but lost on 6 errors
    {"date": "2026-07-16", "away": "Road Dogs", "home": "WCLL 12u All-Stars",
     "away_score": 7, "home_score": 8, "winner": "WCLL 12u All-Stars",
     "field": "Upper Community Field, Lafayette Community Park", "round": "Tournament"},
    # 07/17 — Road Dogs home (batted bottom); five-run LLL first, all 6 runs unearned
    {"date": "2026-07-17", "away": "LLL 12U Tournament Team", "home": "Road Dogs",
     "away_score": 6, "home_score": 1, "winner": "LLL 12U Tournament Team",
     "field": "Buckeye Field, Lafayette", "round": "Tournament"},
    # 07/18 — Road Dogs home (batted bottom); run-ruled after four, shut out
    {"date": "2026-07-18", "away": "LLL 12u All Stars", "home": "Road Dogs",
     "away_score": 12, "home_score": 0, "winner": "LLL 12u All Stars",
     "field": "Upper Community Field, Lafayette Community Park", "round": "Tournament"},
    # 07/19 — Road Dogs away (batted top); Miles D home run, five-hitter
    {"date": "2026-07-19", "away": "Road Dogs", "home": "Piedmont Cobras 12U",
     "away_score": 6, "home_score": 2, "winner": "Road Dogs",
     "field": "Buckeye Field, Lafayette", "round": "Tournament"},
    # 08/08 G1 — Road Dogs home (batted bottom); run-ruled after four, 13 hits
    {"date": "2026-08-08", "away": "No Limit Ohana 12U", "home": "Road Dogs",
     "away_score": 2, "home_score": 13, "winner": "Road Dogs",
     "field": "TBD", "round": "Tournament"},
    # 08/08 G2 — Road Dogs home (batted bottom); seven-run second, run-ruled
    {"date": "2026-08-08", "away": "HBB 12U Summer 2026", "home": "Road Dogs",
     "away_score": 3, "home_score": 12, "winner": "Road Dogs",
     "field": "TBD", "round": "Tournament"},
    # 08/09 — Road Dogs home (batted bottom); Kaleo P home run, Extreme had 17 hits
    {"date": "2026-08-09", "away": "Extreme 12U", "home": "Road Dogs",
     "away_score": 12, "home_score": 9, "winner": "Extreme 12U",
     "field": "TBD", "round": "Tournament"},
]


def get_record():
    wins   = sum(1 for g in GAMES if g["winner"] == "Road Dogs")
    ties   = sum(1 for g in GAMES if g["winner"] == "Tie")
    losses = len(GAMES) - wins - ties
    return wins, losses, ties


def get_runs():
    scored  = sum(g["away_score"] if g["away"] == "Road Dogs" else g["home_score"] for g in GAMES)
    allowed = sum(g["home_score"] if g["away"] == "Road Dogs" else g["away_score"] for g in GAMES)
    return scored, allowed
