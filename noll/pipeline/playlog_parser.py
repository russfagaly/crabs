# playlog_parser.py — 2026 NOLL 12U All-Stars
#
# Parses GameChanger-style play-by-play text exports into structured,
# chronologically-ordered innings/plays for the per-game pages.
#
# Source logs (games/playlogs/<game_id>.txt) are exported in REVERSE
# chronological order — both the inning order (last half-inning first)
# and the play order within each half-inning (last play first). The
# helper get_chronological_innings() reverses both so plays read in
# the order they actually happened.

import re

OUTS_SCORE_RE = re.compile(r"^(CRBS \d+ - [A-Za-z]+ \d+)?( \| )?(\d Outs?)?$")
PITCH_TOKEN_RE = re.compile(r"Ball \d+|Strike \d+(?: looking| swinging)?|Foul(?: Bunt| Tip)?|In play\.?")


def classify(line):
    line = line.strip()
    if not line:
        return "BLANK"
    if OUTS_SCORE_RE.match(line) and (line.startswith("CRBS") or "Out" in line):
        return "OUTS_SCORE"
    if PITCH_TOKEN_RE.search(line):
        return "PITCH_SEQ"
    if "," not in line and "." not in line and len(line) < 30:
        return "HEADER"
    return "DESCRIPTION"


def split_innings(text):
    """Returns list of (half, header, body_text) in file order
    (reverse chronological)."""
    sections = re.split(r"\n(Top \d+(?:st|nd|rd|th) - .+|Bottom \d+(?:st|nd|rd|th) - .+)\n", "\n" + text)
    out = []
    for i in range(1, len(sections), 2):
        header = sections[i]
        body = sections[i + 1]
        half = "Top" if header.startswith("Top") else "Bottom"
        out.append((half, header, body))
    return out


def parse_blocks(body):
    """Returns list of play dicts in file order (reverse chronological
    within the half-inning). Each dict: header, outs_score, pitch_seq, desc."""
    lines = body.split("\n")
    classes = [(l, classify(l)) for l in lines]
    classes = [(l, c) for l, c in classes if c != "BLANK"]
    blocks = []
    i = 0
    while i < len(classes):
        line, c = classes[i]
        if c != "HEADER":
            i += 1
            continue
        header = line
        i += 1
        outs_score = None
        if i < len(classes) and classes[i][1] == "OUTS_SCORE":
            outs_score = classes[i][0]
            i += 1
        pitch_seq = None
        if i < len(classes) and classes[i][1] == "PITCH_SEQ":
            pitch_seq = classes[i][0]
            i += 1
        desc_lines = []
        while i < len(classes) and classes[i][1] == "DESCRIPTION":
            desc_lines.append(classes[i][0])
            i += 1
        blocks.append({"header": header, "outs_score": outs_score,
                        "pitch_seq": pitch_seq, "desc": " ".join(desc_lines)})
    return blocks


def get_chronological_innings(text):
    """Returns list of (half, header, blocks) in chronological order
    (Top 1st first ... last half-inning played last), with each
    inning's blocks also in chronological order."""
    innings = split_innings(text)
    innings = list(reversed(innings))
    result = []
    for half, header, body in innings:
        blocks = list(reversed(parse_blocks(body)))
        result.append((half, header, blocks))
    return result


def load_game_log(game_id):
    """Load and parse games/playlogs/<game_id>.txt. Returns chronological
    innings, or None if no log file exists for this game."""
    import os
    path = os.path.join(os.path.dirname(__file__), "..", "games", "playlogs", f"{game_id}.txt")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        text = f.read()
    return get_chronological_innings(text)
