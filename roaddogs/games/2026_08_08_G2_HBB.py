"""
2026 Road Dogs 12
Opponent: HBB 12U Summer 2026
Date:     08/08 (Game 2)
Round:    Tournament
Result:   W  12-3
Field:    TBD
Note:     Road Dogs were the HOME team (batted bottom). Run-ruled after four on a
          seven-run second. Kaleo P went 2-for-2 with 3 RBI and struck out 8 over
          three innings; Oliver R tripled and doubled for 3 RBI.

Corrected 2026-08-07 from a scorebook check: added a run for Julian W (he has no
hit or walk but was hit by a pitch, so reaching and scoring is consistent), added
strikeouts for Julius N and Miles D, and removed one from Julian W. Every batting
and pitching column reconciles.

The scorebook listed only "Miles" for the extra strikeout. It has to be Miles D,
not Miles M: Miles M had 0 AB in this game (two walks), and a strikeout requires
an at-bat. For the run column "Miles" is the other one — Miles M, who reached on
a walk and scored.
"""
TEAM = "Road Dogs"
DATE = "2026-08-08"

hitting = [
    {"name": "Zach C #3",    "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Huston G #20", "ab": 1, "r": 2, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
    {"name": "Kaleo P #10",  "ab": 2, "r": 2, "h": 2, "rbi": 3, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 2, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 2, "r": 2, "h": 2, "rbi": 3, "bb": 0, "so": 0, "doubles": 1, "triples": 1, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 2, "r": 0, "h": 1, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 1, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 1, "r": 1, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 1, "pqab_bonus": 0},
    {"name": "Miles M #7",   "ab": 0, "r": 1, "h": 0, "rbi": 0, "bb": 2, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 0, "r": 1, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Zeke W #17",   "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 2, "r": 0, "h": 0, "rbi": 1, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Kaleo P #10", "ip": "3.0", "h": 1, "r": 1, "er": 1, "bb": 1, "so": 8, "pitches": 56, "strikes": 31, "bf": 11, "hbp": 1, "hr": 0},
    {"name": "Zach C #3",   "ip": "1.0", "h": 1, "r": 2, "er": 2, "bb": 3, "so": 2, "pitches": 33, "strikes": 15, "bf": 8,  "hbp": 1, "hr": 0},
]
