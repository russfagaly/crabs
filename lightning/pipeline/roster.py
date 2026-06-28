# roster.py — Lafayette Lightning
# Players identified from the 2026-06-06 GRIT game box score.
#
# JERSEY NUMBERS:
#   "jersey" = number confirmed from the GameChanger box score.
#   "jersey" = None  -> PLACEHOLDER. Number not shown in the box score yet.
#                       "confirmed": False flags these for follow-up.
#   Replace None with the real number (and set "confirmed": True) once known.
#
# NOTE: jersey numbers are reference-only — the dashboard matches players by
# name, so placeholders do not affect any stats. They are safe to leave until
# the official roster is available.
#
# Format: {"full": "First L", "short": "First L", "jersey": <int|None>, "confirmed": <bool>}

ROSTER = [
    {"full": "Luca L",    "short": "Luca L",    "jersey": None, "confirmed": False},
    {"full": "Aiden H",   "short": "Aiden H",   "jersey": None, "confirmed": False},
    {"full": "Max C",     "short": "Max C",     "jersey": 22,   "confirmed": True},
    {"full": "Scott C",   "short": "Scott C",   "jersey": 35,   "confirmed": True},
    {"full": "Luke F",    "short": "Luke F",    "jersey": None, "confirmed": False},
    {"full": "Henry M",   "short": "Henry M",   "jersey": None, "confirmed": False},
    {"full": "Jackson B", "short": "Jackson B", "jersey": 21,   "confirmed": True},
    {"full": "William Y", "short": "William Y", "jersey": 12,   "confirmed": True},
    {"full": "Hyland C",  "short": "Hyland C",  "jersey": 18,   "confirmed": True},
    {"full": "Robby F",   "short": "Robby F",   "jersey": None, "confirmed": False},
    {"full": "Tyler R",   "short": "Tyler R",   "jersey": None, "confirmed": False},
]
