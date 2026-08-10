# roster.py — Road Dogs 12 (GameChanger: "Barkers aka Road Dogs 12U")
# Players and jersey numbers confirmed from the 2026-06-13 box scores.
#
# Format: {"full": "First L", "short": "First L", "jersey": <int|None>, "confirmed": <bool>}
#
# #34 displays truncated as "Lennon..." in the box score; the last initial was
# recovered from the SB note in the 06/13 East Bay game ("SB: ... Lennon D ...").

ROSTER = [
    {"full": "Zach C",   "short": "Zach C",   "jersey": 3,  "confirmed": True},
    {"full": "Julius N", "short": "Julius N", "jersey": 30, "confirmed": True},
    {"full": "Sam G",    "short": "Sam G",    "jersey": 12, "confirmed": True},
    {"full": "Oliver R", "short": "Oliver R", "jersey": 13, "confirmed": True},
    {"full": "Miles D",  "short": "Miles D",  "jersey": 24, "confirmed": True},
    {"full": "Carver D", "short": "Carver D", "jersey": 6,  "confirmed": True},
    {"full": "Carter F", "short": "Carter F", "jersey": 5,  "confirmed": True},
    {"full": "Lennon D", "short": "Lennon D", "jersey": 34, "confirmed": True},
    {"full": "Hudson P", "short": "Hudson P", "jersey": 2,  "confirmed": True},
    {"full": "Julian W", "short": "Julian W", "jersey": 22, "confirmed": True},
    {"full": "Jonah M",  "short": "Jonah M",  "jersey": 4,  "confirmed": True},
    {"full": "Sammy E",  "short": "Sammy E",  "jersey": 11, "confirmed": True},
    {"full": "Zeke W",   "short": "Zeke W",   "jersey": 17, "confirmed": True},
    # First appears 07/16 vs WCLL. NOTE: distinct from Miles D #24 — two players
    # named Miles, told apart only by last initial and jersey. Keep both forms
    # exact in game files or their stats will merge.
    {"full": "Miles M",  "short": "Miles M",  "jersey": 7,  "confirmed": True},
    # First appears 07/19 vs Piedmont, where he started and threw 3.2 innings.
    {"full": "Huston G", "short": "Huston G", "jersey": 20, "confirmed": True},
    # First appears 08/08 vs No Limit Ohana: 3-for-3, triple, 4 RBI.
    {"full": "Kaleo P",  "short": "Kaleo P",  "jersey": 10, "confirmed": True},
]
