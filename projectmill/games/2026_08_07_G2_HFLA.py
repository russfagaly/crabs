"""
2026 Project Mill Cooperstown 12U
Opponent: HFLA 12U BLACK
Date:     08/07 (Game 2)
Round:    Cooperstown
Result:   L  5-10
Field:    Cooperstown All Star Village
Note:     Project Mill were the HOME team (batted bottom). Five-run HFLA first
          was the game; run-ruled after four. Noah C hit a solo home run in the
          third. Nine hits and only one strikeout — good contact, wrong innings.

Order confirmed 2026-08-07: the AHQ Illinois win was played first, this game
second. Filename suffix and results.py position are correct as-is.

Every column reconciles against the GameChanger TEAM rows, batting and pitching.
"""
TEAM = "Project Mill"
DATE = "2026-08-07"

hitting = [
    {"name": "Andrew W #22",   "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Noah C #8",      "ab": 2, "r": 1, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 1, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Dylan C #7",     "ab": 2, "r": 2, "h": 2, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Issa R #5",      "ab": 2, "r": 0, "h": 1, "rbi": 2, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Dhilan G #34",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zach B #27",     "ab": 2, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Charlie V #45",  "ab": 2, "r": 1, "h": 2, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Nico Y #18",     "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah L #26",    "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Abraham S #6",   "ab": 1, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #23",   "ab": 0, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
    {"name": "Mark (Jr) G #13","ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Andrew W #22", "ip": "0.2", "h": 3, "r": 5,  "er": 1, "bb": 3, "so": 0, "pitches": 38, "strikes": 16, "bf": 9,  "hbp": 0, "hr": 0},
    {"name": "Dylan C #7",   "ip": "2.2", "h": 6, "r": 5,  "er": 4, "bb": 2, "so": 2, "pitches": 67, "strikes": 40, "bf": 17, "hbp": 1, "hr": 1},
    {"name": "Dhilan G #34", "ip": "0.2", "h": 0, "r": 0,  "er": 0, "bb": 0, "so": 0, "pitches": 2,  "strikes": 2,  "bf": 2,  "hbp": 0, "hr": 0},
]
