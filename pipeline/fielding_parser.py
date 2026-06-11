# fielding_parser.py — 2026 Alameda 12u All-Stars
#
# Best-effort fielding stat extraction (PO, A, DP) from the play-by-play
# logs. Only counts plays where Crabs are on defense (opponent batting)
# AND a Crabs fielder is named in the play description. Many routine
# putouts (unnamed 1B on a 6-3, catcher on a strikeout, etc.) are not
# attributable from the text and are NOT counted — so these totals are
# a floor / minimum, not official totals.

import re
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER
from playlog_parser import get_chronological_innings

# playlog full-name spelling sometimes differs slightly from roster.py
NAME_ALIASES = {
    'Kaleo Pontemayor': 'Kaleo Pontmayor',
}

# All names that can appear in playlogs (roster names + alias spellings),
# longest-first so e.g. "Jordan Cerda-Zein" matches before any substring.
_ALL_NAMES = sorted(
    [p['full'] for p in ROSTER] + list(NAME_ALIASES.keys()),
    key=len, reverse=True
)
NAME_RE = '|'.join(re.escape(n) for n in _ALL_NAMES)

POS_RE = ('pitcher|catcher|first baseman|second baseman|third baseman|'
          'shortstop|left fielder|center fielder|right fielder')

P_DOUBLE_PLAY = re.compile(
    rf'double play,\s*(?:{POS_RE})\s*(?P<n1>{NAME_RE})?\s*to\s*(?:{POS_RE})\s*(?P<n2>{NAME_RE})?'
    rf'(?:\s*to\s*(?:{POS_RE})\s*(?P<n3>{NAME_RE})?)?'
)
P_CAUGHT_STEALING = re.compile(
    rf'caught stealing[^,]*,\s*catcher\s*(?P<n1>{NAME_RE})?\s*to\s*(?:{POS_RE})\s*(?P<n2>{NAME_RE})?'
)
P_FIELDERS_CHOICE = re.compile(
    rf"fielder's choice,?\s*(?:(?:{POS_RE})\s*(?P<n1>{NAME_RE})?\s*to\s*)?(?:{POS_RE})\s*(?P<n2>{NAME_RE})?"
)
P_GROUNDS_OUT_2 = re.compile(
    rf'grounds out,\s*(?:{POS_RE})\s*(?P<n1>{NAME_RE})?\s*to\s*(?:{POS_RE})\s*(?P<n2>{NAME_RE})?'
)
P_GROUNDS_OUT_1 = re.compile(
    rf'grounds out to\s*(?P<pos>{POS_RE})\s*(?P<n1>{NAME_RE})?'
)
P_FLY_POP_LINE = re.compile(
    rf'(?:flies out|pops out|pop out|lines out)(?: in foul territory)? to\s*(?:{POS_RE})\s*(?P<n1>{NAME_RE})?'
)


def _name(short_or_full):
    return NAME_ALIASES.get(short_or_full, short_or_full)


def parse_game_fielding(game_id):
    """Returns dict: full_name -> {'po':int,'a':int,'dp':int} for plays
    where Crabs were on defense and a Crabs fielder was named."""
    stats = {}

    def add(name, key, n=1):
        if not name:
            return
        full = _name(name)
        d = stats.setdefault(full, {'po': 0, 'a': 0, 'dp': 0})
        d[key] += n

    innings = get_chronological_innings_for(game_id)
    if not innings:
        return stats

    for half, header, blocks in innings:
        batting_team = header.split(' - ', 1)[1].strip() if ' - ' in header else ''
        crabs_batting = 'Crabs' in batting_team or 'Alameda' in batting_team
        if crabs_batting:
            continue  # Crabs at bat -> Crabs not fielding, skip

        for b in blocks:
            desc = b.get('desc') or ''
            if not desc:
                continue

            m = P_DOUBLE_PLAY.search(desc)
            if m:
                names = [m.group('n1'), m.group('n2'), m.group('n3')]
                named = [n for n in names if n]
                last = None
                for n in reversed(names):
                    if n:
                        last = n
                        break
                for n in named:
                    add(n, 'dp')
                    if n == last:
                        add(n, 'po')
                    else:
                        add(n, 'a')
                continue

            m = P_CAUGHT_STEALING.search(desc)
            if m:
                add(m.group('n1'), 'a')
                add(m.group('n2'), 'po')
                continue

            m = P_FIELDERS_CHOICE.search(desc)
            if m:
                if m.group('n1'):
                    add(m.group('n1'), 'a')
                add(m.group('n2'), 'po')
                continue

            m = P_GROUNDS_OUT_2.search(desc)
            if m:
                if m.group('n1'):
                    add(m.group('n1'), 'a')
                add(m.group('n2'), 'po')
                continue

            m = P_GROUNDS_OUT_1.search(desc)
            if m:
                if m.group('pos') == 'first baseman':
                    add(m.group('n1'), 'po')
                else:
                    add(m.group('n1'), 'a')
                continue

            m = P_FLY_POP_LINE.search(desc)
            if m:
                add(m.group('n1'), 'po')
                continue

    return stats


def get_chronological_innings_for(game_id):
    path = os.path.join(os.path.dirname(__file__), '..', 'games', 'playlogs', f'{game_id}.txt')
    if not os.path.exists(path):
        return None
    with open(path) as f:
        text = f.read()
    return get_chronological_innings(text)


if __name__ == '__main__':
    import glob
    totals = {}
    for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), '..', 'games', 'playlogs', '*.txt'))):
        gid = os.path.splitext(os.path.basename(path))[0]
        stats = parse_game_fielding(gid)
        print(gid, stats)
        for name, d in stats.items():
            t = totals.setdefault(name, {'po': 0, 'a': 0, 'dp': 0})
            for k in d:
                t[k] += d[k]
    print('\nTOTALS')
    for name, d in sorted(totals.items()):
        print(f"  {name:20s} PO={d['po']:2d} A={d['a']:2d} DP={d['dp']:2d}")
