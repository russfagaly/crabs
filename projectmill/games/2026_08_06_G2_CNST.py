"""
2026 Project Mill Cooperstown 12U
Opponent: Canes Triad Gold 12U
Date:     08/06 (Game 2)
Round:    Cooperstown
Result:   L  10-11
Field:    Cooperstown All Star Village
Note:     Project Mill were the AWAY team (batted top). Led 10-8 into the bottom
          of the 5th; Canes walked it off, with an error scoring three runs.

NOTE: two cells under-read by 1 each. Player RBI rows sum to 5 and SO rows to 6,
while the GameChanger TEAM row reads 6 RBI / 7 SO. AB/R/H/BB and the error total
all reconcile exactly, and total bases tie out at 11 (all singles), so these are
single-cell reads, not scoring anomalies. Rows entered as read — check the Plays
tab and patch the missing RBI and K.
"""
TEAM = "Project Mill"
DATE = "2026-08-06"

hitting = [
    {"name": "Andrew W #22",   "ab": 3, "r": 1, "h": 2, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Noah C #8",      "ab": 3, "r": 2, "h": 3, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 3, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Dhilan G #34",   "ab": 3, "r": 1, "h": 1, "rbi": 2, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Dylan C #7",     "ab": 2, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 1, "pqab_bonus": 0},
    {"name": "Zach B #27",     "ab": 2, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 2, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Nico Y #18",     "ab": 2, "r": 2, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 3, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #23",   "ab": 3, "r": 2, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 2, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Charlie V #45",  "ab": 2, "r": 0, "h": 2, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 1, "pqab_bonus": 0},
    {"name": "Jonah L #26",    "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Abraham S #6",   "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Mark (Jr) G #13","ab": 3, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Noah C #8",     "ip": "3.0", "h": 3, "r": 2,  "er": 2, "bb": 0, "so": 6, "pitches": 48, "strikes": 30, "bf": 12, "hbp": 0, "hr": 0},
    {"name": "Charlie V #45", "ip": "1.2", "h": 6, "r": 7,  "er": 6, "bb": 2, "so": 2, "pitches": 41, "strikes": 23, "bf": 12, "hbp": 0, "hr": 0},
    {"name": "Andrew W #22",  "ip": "0.0", "h": 1, "r": 2,  "er": 0, "bb": 0, "so": 0, "pitches": 7,  "strikes": 5,  "bf": 3,  "hbp": 0, "hr": 0},
]
