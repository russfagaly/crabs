#!/usr/bin/env python3
"""
generate_game_pages.py — 2026 NOLL 12U All-Stars
Reads each game file and produces a per-game page (games/<game_id>.html)
with the NOLL box score (batting + pitching) and the full chronological
play-by-play log, organized by inning with collapsible sections.

Usage:
    cd /path/to/2026_12u_AllStars
    python3 pipeline/generate_game_pages.py

Output: games/<game_id>.html for every games/*.py game file
"""

import sys, os, glob, importlib.util
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER
from results import GAMES
from playlog_parser import load_game_log
import theme

SHORT_TO_FULL = {p['short']: p['full'] for p in ROSTER}


def display_name(name):
    """'A Romero #6' -> full roster name, falling back to the short name."""
    short = name.split(' #')[0]
    return SHORT_TO_FULL.get(short, short)


_now_pt = datetime.now(ZoneInfo("America/Los_Angeles"))
GENERATED = _now_pt.strftime('%B %d, %Y, %-I:%M %p PT')


# ── Load game files ────────────────────────────────────────────────────────────
game_dir = os.path.join(os.path.dirname(__file__), '..', 'games')
games_out_dir = os.path.join(game_dir)

game_files = []
for path in sorted(glob.glob(os.path.join(game_dir, '*.py'))):
    if 'TEMPLATE' in path:
        continue
    spec = importlib.util.spec_from_file_location("g", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"Warning: could not load {path}: {e}")
        continue
    game_id = os.path.splitext(os.path.basename(path))[0]
    date_str = getattr(mod, 'DATE', '')
    if date_str:
        game_files.append((game_id, date_str, mod))

game_files = sorted(game_files, key=lambda x: x[0])

# Match sorted game files to GAMES entries by date order (1:1 chronological)
_games_by_date = defaultdict(list)
for g in GAMES:
    _games_by_date[g['date']].append(g)
_date_idx = defaultdict(int)

game_info = {}  # game_id -> info dict
for game_id, date_str, mod in game_files:
    idx = _date_idx[date_str]
    _date_idx[date_str] += 1
    gs = _games_by_date.get(date_str, [])
    if idx < len(gs):
        g = gs[idx]
        opp  = g['home'] if g['away'] == 'NOLL' else g['away']
        us   = g['away_score'] if g['away'] == 'NOLL' else g['home_score']
        them = g['home_score'] if g['away'] == 'NOLL' else g['away_score']
        res  = 'W' if g['winner'] == 'NOLL' else 'L'
        game_info[game_id] = {
            'opp': opp, 'result': res, 'score': f"{us}-{them}",
            'round': g.get('round', ''), 'date': date_str, 'field': g.get('field', '')
        }


def date_disp(date_str):
    try:
        d = datetime.strptime(date_str, '%Y-%m-%d')
        return d.strftime('%a, %b %-d, %Y')
    except Exception:
        return date_str


def fmt_ip(ip):
    return str(ip)


def cls(val, kind='num'):
    if kind == 'num' and val == 0:
        return 'dim'
    return ''


# ── Build a page for each game ───────────────────────────────────────────────
for i, (game_id, date_str, mod) in enumerate(game_files):
    info = game_info.get(game_id, {})
    opp = info.get('opp', 'TBD')
    result = info.get('result', '')
    score = info.get('score', '')
    round_ = info.get('round', '')
    field = info.get('field', '')

    hitting = getattr(mod, 'hitting', [])
    pitching = getattr(mod, 'pitching', [])

    res_color = 'var(--green)' if result == 'W' else 'var(--red)' if result == 'L' else 'var(--text-muted)'

    # ── Batting table ──
    bat_rows = ''
    totals = defaultdict(int)
    bat_fields = ['ab', 'r', 'h', 'rbi', 'bb', 'so', 'doubles', 'triples', 'hr', 'sb', 'cs', 'e', 'hbp']
    for row in hitting:
        bat_rows += '<tr>'
        bat_rows += f'<td class="name">{display_name(row["name"])}</td>'
        for f in bat_fields:
            v = row.get(f, 0)
            totals[f] += v
            c = 'hi' if f in ('h', 'rbi', 'r') and v > 0 else ('dim' if v == 0 else '')
            bat_rows += f'<td class="{c}">{v}</td>'
        bat_rows += '</tr>\n'
    bat_total_row = '<tr style="font-weight:700;border-top:2px solid var(--border)">'
    bat_total_row += '<td class="name">Team Total</td>'
    for f in bat_fields:
        bat_total_row += f'<td>{totals[f]}</td>'
    bat_total_row += '</tr>\n'

    bat_headers = ['AB', 'R', 'H', 'RBI', 'BB', 'SO', '2B', '3B', 'HR', 'SB', 'CS', 'E', 'HBP']
    bat_head_html = ''.join(f'<th>{h}</th>' for h in bat_headers)

    # ── Pitching table ──
    pitch_rows = ''
    pitch_fields = ['ip', 'h', 'r', 'er', 'bb', 'so', 'pitches', 'strikes', 'bf', 'hbp', 'hr']
    for row in pitching:
        pitch_rows += '<tr>'
        pitch_rows += f'<td class="name">{display_name(row["name"])}</td>'
        for f in pitch_fields:
            v = row.get(f, 0)
            c = 'hi' if f == 'so' and v > 0 else ('dim' if v == 0 else '')
            pitch_rows += f'<td class="{c}">{v}</td>'
        pitch_rows += '</tr>\n'
    pitch_headers = ['IP', 'H', 'R', 'ER', 'BB', 'SO', 'P', 'S', 'BF', 'HBP', 'HR']
    pitch_head_html = ''.join(f'<th>{h}</th>' for h in pitch_headers)

    # ── Play-by-play ──
    innings = load_game_log(game_id)
    pbp_html = ''
    if innings:
        for half, header, blocks in innings:
            label = header.strip()
            pbp_html += '<details class="inning">\n<summary>' + label + '</summary>\n'
            for b in blocks:
                pbp_html += '<div class="play">\n'
                pbp_html += '<div class="play-header"><span>' + b['header'] + '</span>'
                if b['outs_score']:
                    pbp_html += '<span class="tag">' + b['outs_score'] + '</span>'
                pbp_html += '</div>\n'
                if b['pitch_seq']:
                    pbp_html += '<div class="play-pitches">' + b['pitch_seq'] + '</div>\n'
                if b['desc']:
                    pbp_html += '<div class="play-desc">' + b['desc'] + '</div>\n'
                pbp_html += '</div>\n'
            pbp_html += '</details>\n'
    else:
        pbp_html = '<div class="no-games">Play-by-play log not available for this game.</div>'

    # ── Prev / next navigation ──
    prev_link = ''
    next_link = ''
    if i > 0:
        prev_id = game_files[i - 1][0]
        prev_link = f'<a class="game-row" href="{prev_id}.html"><span class="arrow">←</span><span class="opp">Previous game</span></a>'
    if i < len(game_files) - 1:
        next_id = game_files[i + 1][0]
        next_link = f'<a class="game-row" href="{next_id}.html"><span class="opp" style="text-align:right">Next game</span><span class="arrow">→</span></a>'

    title = f"vs {opp} — 2026 NOLL 12U All-Stars"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{theme.head(title)}
</head>
<body>

<div class="header">
  {theme.BACK_LINK}
{theme.THEME_TOGGLE_BUTTON}
  <h1>vs {opp}</h1>
  <div class="sub">{date_disp(date_str)}{' · ' + field if field and field != 'TBD' else ''} · Updated {GENERATED}</div>
  <div class="record">
    <div class="stat"><div class="val" style="color:{res_color}">{result} {score}</div><div class="lbl">{round_}</div></div>
  </div>
</div>

<div class="section">
  <div class="section-title">NOLL Batting</div>
  <div class="tbl-wrap">
    <table>
      <tr><th class="left">Player</th>{bat_head_html}</tr>
      {bat_rows}{bat_total_row}
    </table>
  </div>

  <div class="section-title">NOLL Pitching</div>
  <div class="tbl-wrap">
    <table>
      <tr><th class="left">Player</th>{pitch_head_html}</tr>
      {pitch_rows}
    </table>
  </div>

  <div class="section-title">Play-by-Play</div>
  {pbp_html}

  <div style="display:flex;justify-content:space-between;gap:10px;margin-top:14px">
    {prev_link}{next_link}
  </div>

  <div class="footer">2026 NOLL 12U All-Stars &middot; Generated {GENERATED}</div>
</div>

</body>
</html>"""

    out_path = os.path.join(games_out_dir, f"{game_id}.html")
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"  wrote {out_path}")

print(f"\n✅  {len(game_files)} game pages written to: {games_out_dir}")
