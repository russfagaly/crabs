#!/usr/bin/env python3
"""
generate_scouting.py — 2026 Lafayette Lightning
Builds scouting.html: a Crabs-facing scouting report on Lafayette Lightning,
derived from the same game files that feed the dashboard.

Usage:  python3 pipeline/generate_scouting.py
Output: scouting.html  (sits next to index.html; linked from the dashboard)
"""

import sys, os, glob, importlib.util
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER
from results import GAMES
import theme


def ip_to_dec(s):
    s = str(s)
    if '.' in s:
        w, t = s.split('.')
        return int(w) + int(t) / 3
    return float(s)


def ip_disp(ip):
    w = int(ip); t = round((ip - w) * 3)
    if t == 3:
        w += 1; t = 0
    return f"{w}.{t}"


# ── Load all game files ───────────────────────────────────────────────────────
all_hitting, all_pitching = [], []
game_dir = os.path.join(os.path.dirname(__file__), '..', 'games')
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
    for row in getattr(mod, 'hitting', []):
        all_hitting.append({**row, 'game_id': os.path.basename(path)})
    for row in getattr(mod, 'pitching', []):
        all_pitching.append({**row, 'game_id': os.path.basename(path)})


def display_name(full):
    return full.split(' #')[0]


# ── Aggregate hitting ─────────────────────────────────────────────────────────
H = defaultdict(lambda: {k: 0 for k in
    ['ab','h','bb','hbp','r','rbi','sb','cs','so','doubles','triples','hr','e','pqab_bonus']})
Hgames = defaultdict(set)
for row in all_hitting:
    k = display_name(row['name'])
    for f in H[k]:
        H[k][f] += row.get(f, 0)
    if row.get('ab', 0) or row.get('bb', 0) or row.get('hbp', 0):
        Hgames[k].add(row['game_id'])


def batting(t):
    ab, h, bb, hbp = t['ab'], t['h'], t['bb'], t['hbp']
    pa = ab + bb + hbp
    tb = (h - t['doubles'] - t['triples'] - t['hr']) + 2*t['doubles'] + 3*t['triples'] + 4*t['hr']
    avg = h/ab if ab else 0
    obp = (h+bb+hbp)/pa if pa else 0
    slg = tb/ab if ab else 0
    ops = obp + slg
    iso = slg - avg
    xbh = t['doubles'] + t['triples'] + t['hr']
    kpct = (t['so']/pa*100) if pa else 0
    bbpct = (bb/pa*100) if pa else 0
    rbi = t['rbi']
    qab = min(pa, h + bb + hbp + max(0, rbi - h - bb - hbp) + t['pqab_bonus'])
    qabp = qab/pa if pa else 0
    sbtot = t['sb']; sbpct = (t['sb']/(t['sb']+t['cs'])*100) if (t['sb']+t['cs']) else None
    return dict(pa=pa, ab=ab, h=h, tb=tb, avg=avg, obp=obp, slg=slg, ops=ops, iso=iso,
                xbh=xbh, hr=t['hr'], doubles=t['doubles'], triples=t['triples'],
                r=t['r'], rbi=rbi, bb=bb, so=t['so'], kpct=kpct, bbpct=bbpct,
                sb=sbtot, cs=t['cs'], sbpct=sbpct, e=t['e'], qabp=qabp)


# ── Aggregate pitching ────────────────────────────────────────────────────────
P = defaultdict(lambda: {k: 0 for k in
    ['ipd','h','r','er','bb','so','hr','hbp','pitches','strikes','bf','apps']})
for row in all_pitching:
    k = display_name(row['name'])
    P[k]['ipd'] += ip_to_dec(row.get('ip', '0'))
    for f in ['h','r','er','bb','so','hr','hbp','pitches','strikes','bf']:
        P[k][f] += row.get(f, 0)
    P[k]['apps'] += 1


def pitching(t):
    ip = t['ipd']
    if ip == 0:
        return None
    era = t['er']*9/ip
    whip = (t['h']+t['bb'])/ip
    kip = t['so']/ip
    spct = t['strikes']/t['pitches'] if t['pitches'] else 0
    baa_d = t['bf']-t['bb']-t['hbp']
    baa = t['h']/baa_d if baa_d > 0 else 0
    return dict(apps=t['apps'], ip=ip_disp(ip), ipd=ip, era=era, whip=whip, kip=kip,
                k=t['so'], bb=t['bb'], h=t['h'], hr=t['hr'], hbp=t['hbp'],
                spct=spct, baa=baa, pitches=t['pitches'])


players = []
for p in ROSTER:
    short = p['short']
    _zero = {k: 0 for k in ['ab','h','bb','hbp','r','rbi','sb','cs','so','doubles','triples','hr','e','pqab_bonus']}
    b = batting(H[short] if short in H else _zero)
    b['gp'] = len(Hgames.get(short, set()))
    pit = pitching(P[short]) if short in P else None
    players.append({'name': p['full'], 'b': b, 'p': pit})

# ── Team-level numbers ────────────────────────────────────────────────────────
wins = sum(1 for g in GAMES if g.get('winner') == 'Lafayette')
ties = sum(1 for g in GAMES if g.get('winner') == 'Tie')
losses = len(GAMES) - wins - ties
ng = len(GAMES)
rs = sum(g['away_score'] if g['away'] == 'Lafayette' else g['home_score'] for g in GAMES)
ra = sum(g['home_score'] if g['away'] == 'Lafayette' else g['away_score'] for g in GAMES)
team_hr = sum(pl['b']['hr'] for pl in players)
team_sb = sum(pl['b']['sb'] for pl in players)
team_hr_allowed = sum(pl['p']['hr'] for pl in players if pl['p'])
record_str = f"{wins}-{losses}" + (f"-{ties}" if ties else "")

# Leaders for the narrative
qualified = [pl for pl in players if pl['b']['pa'] >= max(6, ng)]  # ~ regulars
by_ops = sorted(qualified, key=lambda x: -x['b']['ops'])
top_hitters = by_ops[:4]
hr_threats = sorted([pl for pl in players if pl['b']['hr'] > 0], key=lambda x: -x['b']['hr'])
sb_leaders = sorted([pl for pl in players if pl['b']['sb'] > 0], key=lambda x: -x['b']['sb'])
pitchers = sorted([pl for pl in players if pl['p']], key=lambda x: -x['p']['ipd'])
err = sorted([pl for pl in players if pl['b']['e'] > 0], key=lambda x: -x['b']['e'])

GENERATED = datetime.now(ZoneInfo("America/Los_Angeles")).strftime('%B %d, %Y, %-I:%M %p PT')


def fmt3(v):
    if v is None: return '—'
    s = f"{v:.3f}"
    return s.lstrip('0') if s.startswith('0.') else s


def fmt2(v):
    return '—' if v is None else f"{v:.2f}"


def names(lst):
    return ', '.join(pl['name'] for pl in lst)


# ── Build narrative ───────────────────────────────────────────────────────────
top_names = names(top_hitters[:3])
hr_names = names(hr_threats[:4])
sb_total_runners = team_sb
ace = pitchers[0]['name'] if pitchers else '—'

summary_html = f"""
  <p style="margin-bottom:10px"><b style="color:var(--text-strong)">Bottom line:</b>
  A dangerous, streaky <b style="color:var(--text-strong)">bat-first</b> club. Over {ng} Cooperstown games they went
  <b style="color:var(--accent)">{record_str}</b>, scoring <b style="color:var(--text-strong)">{rs}</b> runs
  ({rs/ng:.1f}/game) while allowing <b style="color:var(--text-strong)">{ra}</b> ({ra/ng:.1f}/game).
  They put up double-digit runs repeatedly and mounted multiple late comebacks — they do not stop hitting.
  The way to play them is to <b style="color:var(--text-strong)">limit the big inning</b>: their pitching is hittable and
  walk-prone, so patient, contact-oriented at-bats and pressure on the bases travel well against them.</p>
  <ul style="margin:0 0 4px 18px;color:var(--text-muted);font-size:12px;line-height:1.7">
    <li><b style="color:var(--text-strong)">Pitch carefully to the top of the order.</b> {top_names} are the run producers — work the corners, avoid the middle of the plate, and don't let them beat you with one swing.</li>
    <li><b style="color:var(--text-strong)">Respect the power.</b> {hr_names} have all gone deep; they do real fly-ball damage. Keep the ball down and don't elevate.</li>
    <li><b style="color:var(--text-strong)">Hold the runners.</b> They ran a lot ({sb_total_runners} stolen bases as a team) — a quick clock, varied looks, and a catcher ready to throw will slow them.</li>
    <li><b style="color:var(--text-strong)">Make them throw strikes / make them field.</b> Their arms issued a lot of walks and the defense had miscues; put the ball in play and force plays.</li>
    <li><b style="color:var(--text-strong)">Score early.</b> They've shown they'll claw back — a cushion matters. Don't get into a track meet from behind.</li>
  </ul>
"""

# ── Hitters table (ranked by OPS) ─────────────────────────────────────────────
def cls(v, hi, med):
    if v >= hi: return 'hi'
    if v >= med: return 'med'
    return 'lo'

hitters_rows = ''
for pl in sorted(players, key=lambda x: -x['b']['ops']):
    b = pl['b']
    hitters_rows += (
        f'<tr><td class="name">{pl["name"]}</td>'
        f'<td>{b["gp"]}</td><td>{b["pa"]}</td><td>{b["ab"]}</td><td>{b["h"]}</td>'
        f'<td>{b["hr"]}</td><td>{b["rbi"]}</td>'
        f'<td class="{cls(b["avg"],.400,.300)}">{fmt3(b["avg"])}</td>'
        f'<td class="{cls(b["obp"],.500,.380)}">{fmt3(b["obp"])}</td>'
        f'<td class="{cls(b["slg"],.600,.450)}">{fmt3(b["slg"])}</td>'
        f'<td class="{cls(b["ops"],1.000,.800)}">{fmt3(b["ops"])}</td>'
        f'<td class="{"bad" if b["kpct"]>25 else ""}">{b["kpct"]:.0f}%</td>'
        f'<td>{b["bb"]}</td><td>{b["sb"]}</td>'
        f'</tr>\n'
    )

# ── Pitching table (by workload) ──────────────────────────────────────────────
pit_rows = ''
for pl in pitchers:
    p = pl['p']
    pit_rows += (
        f'<tr><td class="name">{pl["name"]}</td>'
        f'<td>{p["apps"]}</td><td>{p["ip"]}</td>'
        f'<td class="{ "bad" if p["era"]>=6 else "med" if p["era"]>=3 else "hi"}">{fmt2(p["era"])}</td>'
        f'<td class="{ "bad" if p["whip"]>=1.8 else "med" if p["whip"]>=1.2 else "hi"}">{fmt2(p["whip"])}</td>'
        f'<td>{p["k"]}</td><td class="{ "bad" if p["bb"]>=8 else "" }">{p["bb"]}</td>'
        f'<td class="{ "bad" if p["hr"]>=3 else "" }">{p["hr"]}</td>'
        f'<td>{p["pitches"]}</td>'
        f'<td>{p["spct"]*100:.0f}%</td>'
        f'</tr>\n'
    )

# ── Tendency callouts ─────────────────────────────────────────────────────────
kprone = sorted([pl for pl in players if pl['b']['pa'] >= 6 and pl['b']['kpct'] >= 25],
                key=lambda x: -x['b']['kpct'])
def tendency_card(title, body):
    return (f'<div class="card"><div class="player-name">{title}</div>'
            f'<div style="font-size:12px;color:var(--text-muted);line-height:1.6">{body}</div></div>')

power_body = ', '.join(f'{pl["name"]} ({pl["b"]["hr"]} HR)' for pl in hr_threats) or '—'
sb_body = ', '.join(f'{pl["name"]} ({pl["b"]["sb"]})' for pl in sb_leaders[:6]) or '—'
k_body = ', '.join(f'{pl["name"]} ({pl["b"]["kpct"]:.0f}% K)' for pl in kprone) or 'No clear high-strikeout regulars.'
err_body = ', '.join(f'{pl["name"]} ({pl["b"]["e"]} E)' for pl in err) or 'No fielding errors charged.'

cards_html = (
    tendency_card('⚡ Power threats', f'Hit a home run this tournament: {power_body}. Team total: {team_hr} HR.')
    + tendency_card('🏃 Run game', f'They steal aggressively — {sb_body}. Keep them honest.')
    + tendency_card('⚾ Favorable matchups (K-prone)', f'{k_body}.')
    + tendency_card('🧤 Defense to test', f'Spots that booted balls (best-effort, from play-by-play): {err_body}.')
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{theme.head('Scouting — 2026 Lafayette Lightning')}
</head>
<body>

<div class="header">
{theme.THEME_TOGGLE_BUTTON}
  <a class="back-link" href="index.html">← Dashboard</a>
  <h1>📋 Scouting Report — Lafayette Lightning</h1>
  <div class="sub">Crabs prep · Cooperstown {record_str} · Updated {GENERATED}</div>
  <div class="record">
    <div class="stat"><div class="val">{record_str}</div><div class="lbl">Record</div></div>
    <div class="stat"><div class="val">{rs/ng:.1f}</div><div class="lbl">Runs/G For</div></div>
    <div class="stat"><div class="val">{ra/ng:.1f}</div><div class="lbl">Runs/G Against</div></div>
    <div class="stat"><div class="val">{team_hr}</div><div class="lbl">HR Hit</div></div>
    <div class="stat"><div class="val">{team_hr_allowed}</div><div class="lbl">HR Allowed</div></div>
  </div>
</div>

<div class="section">

<div class="section-title">🎯 How to Play Them</div>
<div style="background:var(--info-bg);border:1px solid var(--info-border);border-radius:8px;padding:14px 18px;margin-bottom:18px;color:var(--text)">
{summary_html}
</div>

<div class="section-title">🥎 Hitters — Ranked by OPS</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th><th>GP</th><th>PA</th><th>AB</th><th>H</th><th>HR</th><th>RBI</th>
  <th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>K%</th><th>BB</th><th>SB</th>
</tr></thead><tbody>
{hitters_rows}
</tbody></table></div>

<div class="section-title">⚾ Pitching Staff — by Workload</div>
<div style="color:var(--text-dim);font-size:11px;margin:-6px 0 12px">Lower ERA/WHIP is better. High HR and BB columns are flagged red — these are the exploitable arms.</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th><th>App</th><th>IP</th><th>ERA</th><th>WHIP</th><th>K</th><th>BB</th><th>HR</th><th>Pitches</th><th>Strike%</th>
</tr></thead><tbody>
{pit_rows}
</tbody></table></div>

<div class="section-title">🔑 Tendencies & Matchups</div>
<div class="cards">
{cards_html}
</div>

</div>
<div class="footer">Scouting report · 2026 Lafayette Lightning · Generated {GENERATED} · {ng} games · For Crabs coaching staff</div>
</body></html>"""

out = os.path.join(os.path.dirname(__file__), '..', 'scouting.html')
with open(out, 'w') as f:
    f.write(html)
print(f"✅  Scouting report written to: {os.path.abspath(out)}")
print(f"    Record {record_str} | Top OPS: {by_ops[0]['name'] if by_ops else '—'} | Pitchers: {len(pitchers)}")
