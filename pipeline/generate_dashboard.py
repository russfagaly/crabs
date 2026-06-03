#!/usr/bin/env python3
"""
generate_dashboard.py — 2026 Alameda 12u All-Stars
Reads all game files and produces a standalone dashboard.html.

Usage:
    cd /path/to/2026_12u_AllStars
    python3 pipeline/generate_dashboard.py

Output: dashboard.html (open in any browser, works on mobile)
"""

import sys, os, glob, importlib.util
from collections import defaultdict
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER
from results import GAMES

# ── Little League pitch count rest rules ─────────────────────────────────────
def rest_days_required(pitches):
    if pitches >= 66: return 4
    if pitches >= 51: return 3
    if pitches >= 36: return 2
    if pitches >= 21: return 1
    return 0

def ip_to_dec(s):
    s = str(s)
    if '.' in s:
        w, t = s.split('.')
        return int(w) + int(t) / 3
    return float(s)

def ip_disp(ip):
    w = int(ip); t = round((ip - w) * 3)
    return f"{w}.{t}"

# ── Load all game files ───────────────────────────────────────────────────────
all_hitting  = []
all_pitching = []
game_dates   = set()

game_dir = os.path.join(os.path.dirname(__file__), '..', 'games')
for path in sorted(glob.glob(os.path.join(game_dir, '*.py'))):
    if 'TEMPLATE' in path: continue
    spec = importlib.util.spec_from_file_location("g", path)
    mod  = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"Warning: could not load {path}: {e}")
        continue
    date_str = getattr(mod, 'DATE', '')
    game_dates.add(date_str)
    for row in getattr(mod, 'hitting', []):
        all_hitting.append({**row, 'date': date_str})
    for row in getattr(mod, 'pitching', []):
        all_pitching.append({**row, 'date': date_str})

# ── Build per-player stats ────────────────────────────────────────────────────
def display_name(full_name):
    """Extract 'FirstI L' from game file name format 'First L #N'"""
    return full_name.split(' #')[0]

h_totals = defaultdict(lambda: {
    'ab':0,'h':0,'bb':0,'hbp':0,'r':0,'rbi':0,
    'sb':0,'cs':0,'doubles':0,'triples':0,'hr':0,'games':[]
})
for row in all_hitting:
    key = display_name(row['name'])
    t   = h_totals[key]
    for f in ['ab','h','bb','hbp','r','rbi','sb','cs','doubles','triples','hr']:
        t[f] += row.get(f, 0)
    t['games'].append(row['date'])

p_totals = defaultdict(lambda: {
    'ip':0.,'so':0,'bb':0,'h':0,'er':0,'r':0,
    'bf':0,'hbp':0,'pitches':0,'strikes':0,'apps':0,
    'last_pitched':None,'last_pitches':0,'games':[]
})
for row in all_pitching:
    key = display_name(row['name'])
    t   = p_totals[key]
    ip  = ip_to_dec(row.get('ip','0'))
    t['ip']      += ip
    t['so']      += row.get('so', 0)
    t['bb']      += row.get('bb', 0)
    t['h']       += row.get('h',  0)
    t['er']      += row.get('er', 0)
    t['r']       += row.get('r',  0)
    t['bf']      += row.get('bf', 0)
    t['hbp']     += row.get('hbp',0)
    t['pitches'] += row.get('pitches', 0)
    t['strikes'] += row.get('strikes', 0)
    t['apps']    += 1
    t['games'].append(row['date'])
    # track most recent outing
    if t['last_pitched'] is None or row['date'] > t['last_pitched']:
        t['last_pitched']  = row['date']
        t['last_pitches']  = row.get('pitches', 0)

# ── Last-3-games stats ────────────────────────────────────────────────────────
all_dates = sorted(game_dates)
last3_dates = set(all_dates[-3:]) if len(all_dates) >= 3 else set(all_dates)

l3_hit = defaultdict(lambda: {'ab':0,'h':0,'bb':0,'hbp':0,'r':0,'rbi':0,'sb':0})
for row in all_hitting:
    if row['date'] not in last3_dates: continue
    key = display_name(row['name'])
    t   = l3_hit[key]
    for f in ['ab','h','bb','hbp','r','rbi','sb']:
        t[f] += row.get(f, 0)

# ── Pitch availability ────────────────────────────────────────────────────────
today = date.today()

def pitch_availability(short):
    pt = p_totals.get(short)
    if not pt or pt['last_pitched'] is None:
        return 'available', 'No outings recorded', 0, None
    last = date.fromisoformat(pt['last_pitched'])
    last_pc = pt['last_pitches']
    rest   = rest_days_required(last_pc)
    eligible = last + timedelta(days=rest)
    days_until = (eligible - today).days
    if days_until <= 0:
        status = 'available'
        msg = f"Available — last threw {last_pc}p on {pt['last_pitched']}"
    elif days_until == 1:
        status = 'soon'
        msg = f"Available tomorrow — {last_pc}p on {pt['last_pitched']}"
    else:
        status = 'unavailable'
        msg = f"Available {eligible.strftime('%b %d')} — {last_pc}p on {pt['last_pitched']}"
    return status, msg, last_pc, eligible

# ── Compute derived stats ─────────────────────────────────────────────────────
def batting_line(t):
    ab  = t['ab']; h = t['h']; bb = t['bb']; hbp = t['hbp']
    pa  = ab + bb + hbp
    avg = h/ab if ab > 0 else 0
    obp = (h+bb+hbp)/pa if pa > 0 else 0
    tb  = (h-t['doubles']-t['triples']-t['hr']) + 2*t['doubles'] + 3*t['triples'] + 4*t['hr']
    slg = tb/ab if ab > 0 else 0
    ops = obp + slg
    gp  = len(set(t['games']))
    return dict(gp=gp, pa=pa, ab=ab, h=h, avg=avg, obp=obp, slg=slg, ops=ops,
                r=t['r'], rbi=t['rbi'], bb=bb, sb=t['sb'],
                doubles=t['doubles'], triples=t['triples'], hr=t['hr'], tb=tb)

def pitching_line(t):
    ip = t['ip']
    if ip == 0: return None
    era  = t['er']*9/ip
    whip = (t['h']+t['bb'])/ip
    kip  = t['so']/ip
    baa_d = t['bf']-t['bb']-t['hbp']
    baa  = t['h']/baa_d if baa_d > 0 else 0
    spct = t['strikes']/t['pitches'] if t['pitches'] > 0 else 0
    return dict(apps=t['apps'], ip=ip_disp(ip), ip_d=ip,
                k=t['so'], bb=t['bb'], era=era, whip=whip,
                kip=kip, baa=baa, spct=spct,
                pitches=t['pitches'], strikes=t['strikes'])

# ── Trend arrow ───────────────────────────────────────────────────────────────
def trend(season_ops, l3_ops):
    if l3_ops is None: return '—', '#888'
    diff = l3_ops - season_ops
    if diff >  .100: return '▲', '#22c55e'
    if diff < -.100: return '▼', '#ef4444'
    return '●', '#facc15'

# ── W/L record ────────────────────────────────────────────────────────────────
wins   = sum(1 for g in GAMES if g.get('winner') == 'Alameda')
losses = sum(1 for g in GAMES if g.get('winner') != 'Alameda')
rs     = sum(g['away_score'] if g['away']=='Alameda' else g['home_score'] for g in GAMES) if GAMES else 0
ra     = sum(g['home_score'] if g['away']=='Alameda' else g['away_score'] for g in GAMES) if GAMES else 0

# ── Build player data rows ────────────────────────────────────────────────────
players = []
for p in ROSTER:
    short = p['short']
    ht    = h_totals.get(short, defaultdict(int))
    ht_default = {'ab':0,'h':0,'bb':0,'hbp':0,'r':0,'rbi':0,'sb':0,'cs':0,
                  'doubles':0,'triples':0,'hr':0,'games':[]}
    ht_data = dict(ht_default, **{k:v for k,v in ht.items()})

    bl   = batting_line(ht_data)
    pt   = p_totals.get(short, {})
    pl   = pitching_line(pt) if pt else None
    avail, avail_msg, last_pc, elig = pitch_availability(short)

    l3 = l3_hit.get(short)
    l3_ops = None
    l3_avg = None
    if l3 and l3['ab'] > 0:
        l3pa  = l3['ab']+l3['bb']+l3['hbp']
        l3_obp = (l3['h']+l3['bb']+l3['hbp'])/l3pa if l3pa > 0 else 0
        l3_slg = l3['h']/l3['ab']
        l3_ops = l3_obp + l3_slg
        l3_avg = l3['h']/l3['ab']

    tarrow, tcolor = trend(bl['ops'], l3_ops)

    players.append({
        'full': p['full'], 'short': short,
        'batting': bl, 'pitching': pl,
        'avail': avail, 'avail_msg': avail_msg, 'last_pc': last_pc,
        'elig': elig.strftime('%b %d') if elig and avail != 'available' else '',
        'l3_ops': l3_ops, 'l3_avg': l3_avg,
        'l3_h': l3['h'] if l3 else 0,
        'l3_r': l3['r'] if l3 else 0,
        'l3_rbi': l3['rbi'] if l3 else 0,
        'l3_sb': l3['sb'] if l3 else 0,
        'trend_arrow': tarrow, 'trend_color': tcolor,
    })

# ── HTML generation ───────────────────────────────────────────────────────────
def fmt(val, decimals=3):
    if val is None: return '—'
    if isinstance(val, float):
        s = f"{val:.{decimals}f}"
        return s.lstrip('0') or '0'
    return str(val)

def avail_badge(status):
    colors = {'available': '#22c55e', 'soon': '#facc15', 'unavailable': '#ef4444'}
    labels = {'available': 'AVAILABLE', 'soon': 'TOMORROW', 'unavailable': 'RESTING'}
    c = colors.get(status, '#888')
    l = labels.get(status, status.upper())
    return f'<span style="background:{c};color:#000;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700">{l}</span>'

GENERATED = date.today().strftime('%B %d, %Y')
NUM_GAMES = len(GAMES)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>2026 Alameda 12u All-Stars</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:'Segoe UI',Arial,sans-serif;font-size:14px}}
.header{{background:linear-gradient(135deg,#1e3a5f,#0f172a);padding:20px;text-align:center;border-bottom:2px solid #334155}}
.header h1{{font-size:22px;font-weight:800;color:#f8fafc;letter-spacing:1px}}
.header .sub{{font-size:13px;color:#94a3b8;margin-top:4px}}
.record{{display:flex;gap:24px;justify-content:center;margin-top:14px}}
.record .stat{{text-align:center}}
.record .val{{font-size:28px;font-weight:800;color:#38bdf8}}
.record .lbl{{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:1px}}
.section{{padding:16px;max-width:1100px;margin:0 auto}}
.section-title{{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:2px;
  color:#94a3b8;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #1e293b}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-bottom:24px}}
.card{{background:#1e293b;border-radius:10px;padding:14px;border:1px solid #334155}}
.card.available{{border-color:#22c55e33}}
.card.soon{{border-color:#facc1533}}
.card.unavailable{{border-color:#ef444433}}
.card .player-name{{font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:6px}}
.card .badge-row{{display:flex;align-items:center;gap:8px;margin-bottom:8px}}
.card .pc{{font-size:12px;color:#94a3b8}}
.card .avail-msg{{font-size:11px;color:#64748b;margin-top:4px}}
.card .trend{{font-size:22px;font-weight:800}}
.card .l3-stats{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin-top:10px}}
.card .l3-stat{{text-align:center;background:#0f172a;border-radius:6px;padding:5px 2px}}
.card .l3-val{{font-size:16px;font-weight:700;color:#38bdf8}}
.card .l3-lbl{{font-size:9px;color:#64748b;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:24px}}
th{{background:#1e293b;color:#94a3b8;padding:8px 6px;text-align:center;
   font-weight:600;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid #334155}}
th.left{{text-align:left;padding-left:10px}}
td{{padding:7px 6px;text-align:center;border-bottom:1px solid #1e293b;color:#e2e8f0}}
td.name{{text-align:left;padding-left:10px;font-weight:600;color:#f1f5f9}}
tr:hover td{{background:#1e293b55}}
.hi{{color:#22c55e;font-weight:700}}
.med{{color:#facc15}}
.lo{{color:#94a3b8}}
.bad{{color:#ef4444}}
.game-row{{display:flex;align-items:center;gap:10px;padding:8px 10px;
  background:#1e293b;border-radius:8px;margin-bottom:6px;font-size:13px}}
.game-row .result{{font-weight:800;font-size:14px;min-width:28px}}
.game-row .result.W{{color:#22c55e}}.game-row .result.L{{color:#ef4444}}
.game-row .score{{color:#38bdf8;font-weight:700}}
.game-row .opp{{color:#94a3b8;flex:1}}
.game-row .round{{font-size:10px;color:#64748b;background:#0f172a;padding:2px 6px;border-radius:4px}}
.footer{{text-align:center;padding:20px;font-size:11px;color:#334155}}
.no-games{{text-align:center;padding:40px;color:#475569;font-size:14px}}
@media(max-width:600px){{
  .record{{gap:16px}}.record .val{{font-size:22px}}
  .cards{{grid-template-columns:1fr 1fr}}
  table{{font-size:11px}}th,td{{padding:5px 3px}}
}}
</style>
</head>
<body>

<div class="header">
  <h1>⚾ 2026 Alameda 12u All-Stars</h1>
  <div class="sub">International Team · Updated {GENERATED}</div>
  <div class="record">
    <div class="stat"><div class="val">{wins}-{losses}</div><div class="lbl">Record</div></div>
    <div class="stat"><div class="val">{NUM_GAMES}</div><div class="lbl">Games</div></div>
    <div class="stat"><div class="val">{rs}</div><div class="lbl">Runs For</div></div>
    <div class="stat"><div class="val">{ra}</div><div class="lbl">Runs Against</div></div>
  </div>
</div>

<div class="section">

<!-- BATTING -->
<div class="section-title">🥎 Batting</div>
<table>
<thead><tr>
  <th class="left">Player</th>
  <th>GP</th><th>PA</th><th>AB</th><th>H</th>
  <th>2B</th><th>3B</th><th>HR</th><th>TB</th>
  <th>R</th><th>RBI</th><th>BB</th><th>SB</th>
  <th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th>
</tr></thead><tbody>
"""

for p in sorted(players, key=lambda x: -x['batting']['ops']):
    b = p['batting']
    def cls(val, hi, med):
        if val >= hi:  return 'hi'
        if val >= med: return 'med'
        return 'lo'
    html += f"""<tr>
  <td class="name">{p['full']}</td>
  <td>{b['gp']}</td><td>{b['pa']}</td><td>{b['ab']}</td><td>{b['h']}</td>
  <td>{b['doubles']}</td><td>{b['triples']}</td><td>{b['hr']}</td><td>{b['tb']}</td>
  <td>{b['r']}</td><td>{b['rbi']}</td><td>{b['bb']}</td><td>{b['sb']}</td>
  <td class="{cls(b['avg'],.400,.300)}">{fmt(b['avg'])}</td>
  <td class="{cls(b['obp'],.500,.380)}">{fmt(b['obp'])}</td>
  <td class="{cls(b['slg'],.600,.450)}">{fmt(b['slg'])}</td>
  <td class="{cls(b['ops'],1.000,.800)}">{fmt(b['ops'])}</td>
</tr>"""

html += """</tbody></table>

<!-- PITCHING -->
<div class="section-title">⚾ Pitching</div>
<table>
<thead><tr>
  <th class="left">Player</th>
  <th>App</th><th>IP</th><th>K</th><th>BB</th>
  <th>ERA</th><th>WHIP</th><th>K/IP</th><th>BAA</th><th>Strike%</th><th>Pitches</th>
</tr></thead><tbody>
"""

pit_players = [(p, p['pitching']) for p in players if p['pitching']]
pit_players.sort(key=lambda x: x[1]['era'])
for p, pl in pit_players:
    def pcls(val, good, ok, flip=False):
        if flip:
            if val <= good: return 'hi'
            if val <= ok:   return 'med'
            return 'bad'
        else:
            if val >= good: return 'hi'
            if val >= ok:   return 'med'
            return 'lo'
    html += f"""<tr>
  <td class="name">{p['full']}</td>
  <td>{pl['apps']}</td><td>{pl['ip']}</td>
  <td class="{pcls(pl['kip'],1.5,1.0)}">{pl['k']}</td>
  <td>{pl['bb']}</td>
  <td class="{pcls(pl['era'],3.0,6.0,flip=True)}">{fmt(pl['era'],2)}</td>
  <td class="{pcls(pl['whip'],1.2,1.8,flip=True)}">{fmt(pl['whip'],2)}</td>
  <td class="{pcls(pl['kip'],1.5,1.0)}">{fmt(pl['kip'],2)}</td>
  <td class="{pcls(pl['baa'],.200,.300,flip=True)}">{fmt(pl['baa'])}</td>
  <td class="{pcls(pl['spct'],.65,.58)}">{pl['spct']:.1%}</td>
  <td>{pl['pitches']}</td>
</tr>"""

html += """</tbody></table>

<!-- PITCHING AVAILABILITY -->
<div class="section-title">⚡ Pitching Availability</div>
<div class="cards">
"""

for p in sorted(players, key=lambda x: (
    0 if x['avail']=='available' else 1 if x['avail']=='soon' else 2,
    x['full']
)):
    pl = p['pitching']
    season_ip = pl['ip'] if pl else '—'
    html += f"""
  <div class="card {p['avail']}">
    <div class="player-name">{p['full']}</div>
    <div class="badge-row">{avail_badge(p['avail'])}<span class="pc">{'Last: ' + str(p['last_pc']) + 'p' if p['last_pc'] else 'No outings'}</span></div>
    {'<div class="avail-msg">Eligible: ' + p['elig'] + '</div>' if p['elig'] else ''}
    <div class="avail-msg">Season IP: {season_ip} · K: {pl['k'] if pl else '—'}</div>
  </div>"""

html += """
</div>

<!-- HOT/COLD TRACKER -->
<div class="section-title">🔥 Last 3 Games — Hot/Cold Tracker</div>
<div class="cards">
"""

for p in sorted(players, key=lambda x: -(x['l3_ops'] or 0)):
    l3_avg_s = fmt(p['l3_avg']) if p['l3_avg'] is not None else '—'
    l3_ops_s = fmt(p['l3_ops']) if p['l3_ops'] is not None else '—'
    html += f"""
  <div class="card">
    <div class="player-name">{p['full']}</div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
      <span class="trend" style="color:{p['trend_color']}">{p['trend_arrow']}</span>
      <div>
        <div style="font-size:11px;color:#64748b">L3 OPS</div>
        <div style="font-size:18px;font-weight:800;color:#38bdf8">{l3_ops_s}</div>
      </div>
      <div style="margin-left:auto;text-align:right">
        <div style="font-size:11px;color:#64748b">Season</div>
        <div style="font-size:13px;color:#94a3b8">{fmt(p['batting']['ops'])}</div>
      </div>
    </div>
    <div class="l3-stats">
      <div class="l3-stat"><div class="l3-val">{l3_avg_s}</div><div class="l3-lbl">AVG</div></div>
      <div class="l3-stat"><div class="l3-val">{p['l3_r']}</div><div class="l3-lbl">R</div></div>
      <div class="l3-stat"><div class="l3-val">{p['l3_rbi']}</div><div class="l3-lbl">RBI</div></div>
    </div>
  </div>"""

html += """
</div>

<!-- GAME LOG -->
<div class="section-title">📋 Game Log</div>
"""

if not GAMES:
    html += '<div class="no-games">No games recorded yet. Add results to pipeline/results.py</div>'
else:
    for g in reversed(GAMES):
        alameda_score = g['away_score'] if g['away']=='Alameda' else g['home_score']
        opp_score     = g['home_score'] if g['away']=='Alameda' else g['away_score']
        opp_name      = g['home'] if g['away']=='Alameda' else g['away']
        result        = 'W' if g['winner']=='Alameda' else 'L'
        rnd           = g.get('round','')
        field         = g.get('field','')
        html += f"""<div class="game-row">
  <span class="result {result}">{result}</span>
  <span class="score">{alameda_score}–{opp_score}</span>
  <span class="opp">vs {opp_name}{' · ' + field if field else ''}</span>
  <span>{g['date']}</span>
  {'<span class="round">' + rnd + '</span>' if rnd else ''}
</div>"""

html += f"""
</div>

<div class="footer">2026 Alameda 12u All-Stars · Generated {GENERATED} · {NUM_GAMES} games</div>
</body></html>"""

# ── Write output ──────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard.html')
with open(out_path, 'w') as f:
    f.write(html)

print(f"✅  Dashboard written to: {os.path.abspath(out_path)}")
print(f"    Games: {NUM_GAMES}  |  Record: {wins}-{losses}  |  Players: {len(ROSTER)}")
