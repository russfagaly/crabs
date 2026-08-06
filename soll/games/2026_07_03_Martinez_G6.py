"""
2026 SOLL 12U All-Stars
Opponent: Martinez 12U All-Stars
Date:     07/03
Round:    Districts
Result:   L  1-4
Field:    TBD

NOTE: player SO rows sum to 6; the GameChanger TEAM row reads 7. AB/R/H/RBI/BB/E
all reconcile exactly, so this is a single-cell read, not a scoring anomaly (a
missing batter would raise AB too). Rows entered as read. Check the Plays tab and
patch the one SO if it turns out to be 7.
"""
TEAM = "SOLL"
DATE = "2026-07-03"

hitting = [
    {"name": "Lorenzo A #7",  "ab": 3, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Julian Y #3",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 2, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Cameron B #14", "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Wiley O #11",   "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Caiden R #12",  "ab": 2, "r": 1, "h": 2, "rbi": 1, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 1, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Reed H #10",    "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Arlo B #5",     "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Elias G #4",    "ab": 2, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 2, "hbp": 0, "pqab_bonus": 0},
    {"name": "Malikiel O #13","ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 1, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 1, "hbp": 0, "pqab_bonus": 0},
    {"name": "Clive A #8",    "ab": 2, "r": 0, "h": 1, "rbi": 0, "bb": 0, "so": 0, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
    {"name": "Thiago S #9",   "ab": 1, "r": 0, "h": 0, "rbi": 0, "bb": 0, "so": 1, "doubles": 0, "triples": 0, "hr": 0, "sb": 0, "cs": 0, "e": 0, "hbp": 0, "pqab_bonus": 0},
]

pitching = [
    {"name": "Clive A #8", "ip": "5.0", "h": 3, "r": 4, "er": 1, "bb": 0, "so": 8, "pitches": 86, "strikes": 58, "bf": 24, "hbp": 2, "hr": 0},
]
