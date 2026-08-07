"""
2026 Road Dogs 12
Opponent: Delta Valley Bruins 12U
Date:     06/14
Round:    Tournament
Result:   L  7-10
Field:    TBD
Note:     Road Dogs were the HOME team (batted bottom). Oliver R homered to left
          in the 2nd. Delta Valley broke it open with four in the 6th.

Jonah M's hit was recovered from the TB note ("Jonah M 1") — the lineup row read
as 0 H, but with his single the hit total reconciles to the TEAM row's 9, and
total bases tie out at 15 against the 3 doubles + Oliver R's home run.

Corrected 2026-08-07 from a scorebook check: removed an RBI from Carter F
(RBI now 7). Every batting and pitching column reconciles.
"""
TEAM = "Road Dogs"
DATE = "2026-06-14"

hitting = [
    {"name": "Zach C #3",    "ab": 3, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 1, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julius N #30", "ab": 2, "r": 0, "h": 1, "rbi": 1, "bb": 1, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sam G #12",    "ab": 3, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carter F #5",  "ab": 2, "r": 1, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Oliver R #13", "ab": 1, "r": 2, "h": 1, "rbi": 2, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 1, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Sammy E #11",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Jonah M #4",   "ab": 2, "r": 2, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Carver D #6",  "ab": 2, "r": 1, "h": 2, "rbi": 2, "bb": 0, "so": 0, "doubles": 1, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Lennon D #34", "ab": 2, "r": 0, "h": 1, "rbi": 2, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Miles D #24",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Hudson P #2",  "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian W #22", "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Sam G #12",    "ip": "1.1", "h": 3, "r": 3, "er": 1, "bb": 1, "so": 2, "pitches": 41, "strikes": 19, "bf": 11, "hbp": 2, "hr": 0},
    {"name": "Lennon D #34", "ip": "4.2", "h": 9, "r": 7, "er": 2, "bb": 3, "so": 4, "pitches": 87, "strikes": 57, "bf": 27, "hbp": 0, "hr": 0},
]
