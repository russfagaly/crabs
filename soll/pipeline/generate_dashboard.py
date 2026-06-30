#!/usr/bin/env python3
"""
generate_dashboard.py — 2026 SOLL 12U All-Stars
Reads all game files and produces a standalone dashboard.html.

Usage:
    cd /path/to/2026_12u_AllStars
    python3 pipeline/generate_dashboard.py

Output: dashboard.html (open in any browser, works on mobile)
"""

import sys, os, glob, importlib.util
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER
from results import GAMES
from fielding_parser import parse_game_fielding
import theme

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
game_ids     = []   # list of (game_id, date_str) in sorted order
game_log_by_id = {}  # game_id -> {opp, result, score, round, date}

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
    game_id  = os.path.splitext(os.path.basename(path))[0]
    date_str = getattr(mod, 'DATE', '')
    if date_str:
        game_ids.append((game_id, date_str))
    for idx, row in enumerate(getattr(mod, 'hitting', [])):
        all_hitting.append({**row, 'game_id': game_id, 'date': date_str, 'lineup_pos': idx + 1})
    for row in getattr(mod, 'pitching', []):
        all_pitching.append({**row, 'game_id': game_id, 'date': date_str})

game_ids = sorted(game_ids, key=lambda x: x[0])

# ── Fielding stats (best-effort, from play-by-play; PO/A/DP are minimums —
# many unnamed routine plays can't be attributed) ─────────────────────────────
field_totals = defaultdict(lambda: {'po': 0, 'a': 0, 'dp': 0})
for game_id, _ in game_ids:
    for full_name, d in parse_game_fielding(game_id).items():
        for k in d:
            field_totals[full_name][k] += d[k]

# Per-game-id label suffix, e.g. " (G2)" for doubleheaders on the same date
game_label_suffix = {}
_date_game_count = defaultdict(int)
for game_id, date_str in game_ids:
    _date_game_count[date_str] += 1
    n = sum(1 for _, d in game_ids if d == date_str)
    game_label_suffix[game_id] = f' (G{_date_game_count[date_str]})' if n > 1 else ''

# Build game info lookup — match sorted game files to GAMES entries by date order
_games_by_date = defaultdict(list)
for g in GAMES:
    _games_by_date[g['date']].append(g)
_date_idx = defaultdict(int)
game_id_by_game = {}  # id(g) -> game_id, for linking Game Log rows to per-game pages
for game_id, date_str in game_ids:
    idx = _date_idx[date_str]
    _date_idx[date_str] += 1
    gs = _games_by_date.get(date_str, [])
    if idx < len(gs):
        g = gs[idx]
        opp  = g['home'] if g['away'] == 'SOLL' else g['away']
        us   = g['away_score'] if g['away'] == 'SOLL' else g['home_score']
        them = g['home_score'] if g['away'] == 'SOLL' else g['away_score']
        res  = 'W' if g['winner'] == 'SOLL' else 'L'
        game_log_by_id[game_id] = {'opp': opp, 'result': res, 'score': f"{us}-{them}",
                                    'round': g.get('round', ''), 'date': date_str}
        game_id_by_game[id(g)] = game_id

# ── Build per-player stats ────────────────────────────────────────────────────
def display_name(full_name):
    return full_name.split(' #')[0]

h_totals = defaultdict(lambda: {
    'ab':0,'h':0,'bb':0,'hbp':0,'r':0,'rbi':0,
    'sb':0,'cs':0,'so':0,'doubles':0,'triples':0,'hr':0,'e':0,'pqab_bonus':0,'games':[]
})
for row in all_hitting:
    key = display_name(row['name'])
    t   = h_totals[key]
    for f in ['ab','h','bb','hbp','r','rbi','sb','cs','so','doubles','triples','hr','e','pqab_bonus']:
        t[f] += row.get(f, 0)
    t['games'].append(row['game_id'])

# Per-batting-order-position totals: lineup_totals[short][pos] = {ab,h,bb,hbp}
lineup_totals = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
max_lineup_pos = 0
for row in all_hitting:
    key = display_name(row['name'])
    pos = row['lineup_pos']
    max_lineup_pos = max(max_lineup_pos, pos)
    for f in ['ab', 'h', 'bb', 'hbp']:
        lineup_totals[key][pos][f] += row.get(f, 0)

# Per-game hitting log per player
player_game_log = defaultdict(dict)  # short -> {game_id -> stats}
for row in all_hitting:
    key = display_name(row['name'])
    gid = row['game_id']
    if gid not in player_game_log[key]:
        player_game_log[key][gid] = defaultdict(int)
    for f in ['ab','h','bb','hbp','r','rbi','sb','cs','so','doubles','triples','hr','e']:
        player_game_log[key][gid][f] += row.get(f, 0)

player_pitch_log = defaultdict(dict)  # short -> {game_id -> stats}
for row in all_pitching:
    key = display_name(row['name'])
    gid = row['game_id']
    ip  = ip_to_dec(row.get('ip', '0'))
    if gid not in player_pitch_log[key]:
        player_pitch_log[key][gid] = defaultdict(int)
        player_pitch_log[key][gid]['ip'] = 0.
    player_pitch_log[key][gid]['ip'] += ip
    for f in ['h','r','er','bb','so','hr','hbp','pitches','strikes','bf']:
        player_pitch_log[key][gid][f] += row.get(f, 0)

p_totals = defaultdict(lambda: {
    'ip':0.,'so':0,'bb':0,'h':0,'er':0,'r':0,'hr':0,
    'bf':0,'hbp':0,'pitches':0,'strikes':0,'apps':0,
    'last_pitched':None,'last_pitches':0,'last_date':None,
    'outings':[]
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
    t['hr']      += row.get('hr', 0)
    t['bf']      += row.get('bf', 0)
    t['hbp']     += row.get('hbp',0)
    t['pitches'] += row.get('pitches', 0)
    t['strikes'] += row.get('strikes', 0)
    t['apps']    += 1
    pc = row.get('pitches', 0)
    d  = row['date']
    t['outings'].append({'date': d, 'pitches': pc, 'ip': ip_disp(ip)})
    if t['last_date'] is None or d > t['last_date']:
        t['last_date']    = d
        t['last_pitches'] = pc

# ── Last-3-games stats ────────────────────────────────────────────────────────
# L3 stats computed per-player in the player loop below (each player's own last 3 appearances)

# ── Pitch availability ────────────────────────────────────────────────────────
today = date.today()

def pitch_availability(short):
    pt = p_totals.get(short)
    if not pt or pt['last_date'] is None:
        return 'available', 'No outings recorded', 0, None
    last     = date.fromisoformat(pt['last_date'])
    last_pc  = pt['last_pitches']
    rest     = rest_days_required(last_pc)
    eligible = last + timedelta(days=rest)
    days_until = (eligible - today).days
    if days_until <= 0:
        return 'available', f"Available — last threw {last_pc}p on {pt['last_date']}", last_pc, eligible
    elif days_until == 1:
        return 'soon', f"Available tomorrow — {last_pc}p on {pt['last_date']}", last_pc, eligible
    else:
        return 'unavailable', f"Available {eligible.strftime('%b %d')} — {last_pc}p on {pt['last_date']}", last_pc, eligible

# ── Computed batting stats ────────────────────────────────────────────────────
def batting_line(t):
    ab=t['ab']; h=t['h']; bb=t['bb']; hbp=t['hbp']
    pa=ab+bb+hbp; so=t['so']; cs=t['cs']; sb=t['sb']
    avg=h/ab if ab>0 else 0
    obp=(h+bb+hbp)/pa if pa>0 else 0
    tb=(h-t['doubles']-t['triples']-t['hr'])+2*t['doubles']+3*t['triples']+4*t['hr']
    slg=tb/ab if ab>0 else 0
    ops=obp+slg; iso=slg-avg; xbh=t['doubles']+t['triples']+t['hr']
    sbpct=(sb/(sb+cs)*100) if (sb+cs)>0 else None
    bbpct=(bb/pa*100) if pa>0 else 0
    kpct=(so/pa*100) if pa>0 else 0
    gp=len(set(t['games']))
    # QAB — partial count: H, BB, HBP are always distinct qualifying PAs;
    # RBIs on outs estimated as max(0, rbi − h − bb − hbp);
    # pqab_bonus adds hard-hit-ball outs (line drives / hard grounders & fly balls)
    # identified from play-by-play logs, where available.
    rbi=t['rbi']
    pqab_bonus = t.get('pqab_bonus', 0)
    qab = min(pa, h + bb + hbp + max(0, rbi - h - bb - hbp) + pqab_bonus)
    qab_pct = qab/pa if pa>0 else 0
    return dict(gp=gp,pa=pa,ab=ab,h=h,avg=avg,obp=obp,slg=slg,ops=ops,iso=iso,
                r=t['r'],rbi=rbi,bb=bb,hbp=hbp,so=so,sb=sb,cs=cs,
                sbpct=sbpct,bbpct=bbpct,kpct=kpct,
                doubles=t['doubles'],triples=t['triples'],hr=t['hr'],
                tb=tb,xbh=xbh,e=t['e'],qab=qab,qab_pct=qab_pct,pqab_bonus=pqab_bonus)

FIP_CONSTANT = 3.10  # standard-ish constant; not league-calibrated for 12U

def pitching_line(t):
    ip=t['ip']
    if ip==0: return None
    era=t['er']*9/ip; whip=(t['h']+t['bb'])/ip; kip=t['so']/ip
    baa_d=t['bf']-t['bb']-t['hbp']; baa=t['h']/baa_d if baa_d>0 else 0
    spct=t['strikes']/t['pitches'] if t['pitches']>0 else 0
    kbb=t['so']/t['bb'] if t['bb']>0 else None
    fip=(13*t['hr'] + 3*(t['bb']+t['hbp']) - 2*t['so'])/ip + FIP_CONSTANT
    return dict(apps=t['apps'],ip=ip_disp(ip),ip_d=ip,
                k=t['so'],bb=t['bb'],h=t['h'],r=t['r'],er=t['er'],hbp=t['hbp'],hr=t['hr'],
                era=era,whip=whip,kip=kip,baa=baa,spct=spct,kbb=kbb,fip=fip,
                pitches=t['pitches'],last_pc=t['last_pitches'],last_date=t['last_date'],
                outings=t['outings'])

def heat_status(l3_ops):
    """Classify a player's last-3-games OPS as hot/steady/cold on its own
    merits (not relative to season average)."""
    if l3_ops is None: return '—', 'var(--text-dim)', 'NO DATA'
    if l3_ops >= 1.000: return '🔥', 'var(--green)', 'HOT'
    if l3_ops >= 0.600: return '●', 'var(--yellow)', 'STEADY'
    return '❄️', 'var(--red)', 'COLD'

# ── W/L record ────────────────────────────────────────────────────────────────
wins   = sum(1 for g in GAMES if g.get('winner')=='SOLL')
losses = sum(1 for g in GAMES if g.get('winner')!='SOLL')
rs     = sum(g['away_score'] if g['away']=='SOLL' else g['home_score'] for g in GAMES) if GAMES else 0
ra     = sum(g['home_score'] if g['away']=='SOLL' else g['away_score'] for g in GAMES) if GAMES else 0

# ── Pythagorean W-L (exponent 1.83, per Bill James) ──────────────────────────
if rs > 0 or ra > 0:
    _exp = 1.83
    pythag_pct = rs**_exp / (rs**_exp + ra**_exp)
    _g = wins + losses
    pythag_w = round(pythag_pct * _g, 1)
    pythag_l = round((1 - pythag_pct) * _g, 1)
    pythag_str = f"{pythag_w:.1f}-{pythag_l:.1f}"
else:
    pythag_str = '—'

# ── Build player data rows ────────────────────────────────────────────────────
players = []
for p in ROSTER:
    short = p['short']
    ht    = h_totals.get(short, {})
    ht_d  = {k: ht.get(k,0) for k in ['ab','h','bb','hbp','r','rbi','sb','cs','so','doubles','triples','hr','e','pqab_bonus']}
    ht_d['games'] = ht.get('games',[])
    bl   = batting_line(ht_d)
    pt   = p_totals.get(short, {})
    pl   = pitching_line(pt) if pt else None
    avail, avail_msg, last_pc, elig = pitch_availability(short)

    # Last 3 games this player actually appeared in
    player_gids = [gid for gid, _ in game_ids
                   if (player_game_log[short].get(gid, {}).get('ab', 0) > 0
                       or player_game_log[short].get(gid, {}).get('bb', 0) > 0
                       or player_game_log[short].get(gid, {}).get('hbp', 0) > 0)]
    last3_player_ids = set(player_gids[-3:])
    l3 = defaultdict(int)
    for gid in last3_player_ids:
        for f in ['ab','h','bb','hbp','r','rbi','sb','so']:
            l3[f] += player_game_log[short].get(gid, {}).get(f, 0)
    l3_ops=None; l3_avg=None
    if l3.get('ab',0)>0:
        l3pa=(l3['ab']+l3['bb']+l3['hbp'])
        l3_obp=(l3['h']+l3['bb']+l3['hbp'])/l3pa if l3pa>0 else 0
        l3_slg=l3['h']/l3['ab']
        l3_ops=l3_obp+l3_slg; l3_avg=l3['h']/l3['ab']

    hicon,hcolor,hlabel = heat_status(l3_ops)

    # Per-game log for this player
    pg = []
    for game_id, date_str in game_ids:
        gs = player_game_log[short].get(game_id, {})
        ab=gs.get('ab',0); h=gs.get('h',0); bb=gs.get('bb',0); hbp=gs.get('hbp',0)
        pa=ab+bb+hbp
        avg=h/ab if ab>0 else None
        tb=(h-gs.get('doubles',0)-gs.get('triples',0)-gs.get('hr',0))+2*gs.get('doubles',0)+3*gs.get('triples',0)+4*gs.get('hr',0)
        slg=tb/ab if ab>0 else None
        obp=(h+bb+hbp)/pa if pa>0 else None
        ops=(obp+slg) if (obp is not None and slg is not None) else None
        gi = game_log_by_id.get(game_id, {})
        pg.append({'date':date_str,'game_id':game_id,'ab':ab,'h':h,'r':gs.get('r',0),'rbi':gs.get('rbi',0),
                   'bb':bb,'hbp':hbp,'sb':gs.get('sb',0),'so':gs.get('so',0),
                   'avg':avg,'ops':ops,'opp':gi.get('opp',''),'result':gi.get('result',''),
                   'score':gi.get('score',''),'dnp':ab==0 and bb==0 and hbp==0})

    # Per-game pitching log for this player
    pgp = []
    for game_id, date_str in game_ids:
        ps = player_pitch_log.get(short, {}).get(game_id)
        if ps:
            pgp.append({'date':date_str,'game_id':game_id,'pitched':True,
                        'ip':ip_disp(ps['ip']),'h':ps['h'],'r':ps['r'],'er':ps['er'],
                        'bb':ps['bb'],'so':ps['so'],'hr':ps['hr'],'hbp':ps['hbp'],
                        'pitches':ps['pitches'],'strikes':ps['strikes'],'bf':ps['bf']})
        else:
            pgp.append({'date':date_str,'game_id':game_id,'pitched':False})

    # Fielding (best-effort from play-by-play; PO/A/DP are minimums)
    fpo = field_totals[p['full']]['po']
    fa  = field_totals[p['full']]['a']
    fdp = field_totals[p['full']]['dp']
    fchances = fpo + fa + bl['e']
    fpct = (fpo + fa) / fchances if fchances > 0 else None
    field = {'po':fpo,'a':fa,'dp':fdp,'pct':fpct}

    players.append({
        'full':p['full'],'short':short,'batting':bl,'pitching':pl,'field':field,
        'avail':avail,'avail_msg':avail_msg,'last_pc':last_pc,
        'elig':elig.strftime('%b %d') if elig and avail!='available' else '',
        'l3_ops':l3_ops,'l3_avg':l3_avg,
        'l3_h':l3.get('h',0),'l3_r':l3.get('r',0),'l3_rbi':l3.get('rbi',0),'l3_sb':l3.get('sb',0),
        'heat_icon':hicon,'heat_color':hcolor,'heat_label':hlabel,'per_game':pg,'per_game_pitch':pgp,
    })

# ── HTML helpers ──────────────────────────────────────────────────────────────
def fmt(val, decimals=3):
    if val is None: return '—'
    if isinstance(val, float):
        s = f"{val:.{decimals}f}"
        return s.lstrip('0') or '0'
    return str(val)

def fmt_lz(val, decimals=2):
    """Format a float keeping the leading zero (e.g. ERA, WHIP)."""
    if val is None: return '—'
    return f"{val:.{decimals}f}"

def pct(val, dec=1):
    if val is None: return '—'
    return f"{val:.{dec}f}%"

def avail_badge(status, elig_date=''):
    colors={'available':'var(--green)','soon':'var(--yellow)','unavailable':'var(--red)'}
    if status == 'available':
        label = 'AVAILABLE'
    else:
        label = elig_date if elig_date else ('TOMORROW' if status == 'soon' else 'RESTING')
    c = colors.get(status, '#888')
    return f'<span style="background:{c};color:#000;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700">{label}</span>'

# ── pQAB table rows ──────────────────────────────────────────────────────────
def _pqab_cls(pct_val):
    if pct_val >= .55: return 'hi'   # elite for 12U travel
    if pct_val >= .40: return 'med'  # average for 12U travel
    return 'lo'

pqab_rows_html = ''
team_pa_total = team_qab_total = 0
for p in sorted(players, key=lambda x: -x['batting']['qab_pct']):
    b = p['batting']
    team_pa_total  += b['pa']
    team_qab_total += b['qab']
    pqab_rows_html += (
        f'<tr><td class="name">{p["full"]}</td>'
        f'<td>{b["pa"]}</td><td>{b["h"]}</td><td>{b["bb"]}</td><td>{b["hbp"]}</td><td>{b["pqab_bonus"]}</td>'
        f'<td class="{_pqab_cls(b["qab_pct"])}">{b["qab"]}</td>'
        f'<td class="{_pqab_cls(b["qab_pct"])}">{b["qab_pct"]:.1%}</td>'
        f'</tr>\n'
    )
team_qab_pct = team_qab_total / team_pa_total if team_pa_total > 0 else 0
pqab_rows_html += (
    f'<tr style="font-weight:700;border-top:2px solid var(--border)">'
    f'<td class="name">TEAM</td>'
    f'<td>{team_pa_total}</td><td></td><td></td><td></td><td></td>'
    f'<td class="{_pqab_cls(team_qab_pct)}">{team_qab_total}</td>'
    f'<td class="{_pqab_cls(team_qab_pct)}">{team_qab_pct:.1%}</td>'
    f'</tr>\n'
)

# ── Lineup position heatmap ───────────────────────────────────────────────────
def _lineup_cls(ab, h):
    if ab == 0: return 'lo'
    avg = h / ab
    if avg >= .400: return 'hi'
    if avg >= .300: return 'med'
    return 'lo'

lineup_header_html = ''.join(f'<th>{i}</th>' for i in range(1, max_lineup_pos + 1))

lineup_rows_html = ''
for p in sorted(players, key=lambda x: x['full']):
    short = p['short']
    lineup_rows_html += f'<tr><td class="name">{p["full"]}</td>'
    for pos in range(1, max_lineup_pos + 1):
        d = lineup_totals.get(short, {}).get(pos)
        if not d or (d['ab'] == 0 and d['bb'] == 0 and d['hbp'] == 0):
            lineup_rows_html += '<td class="dim">—</td>'
        elif d['ab'] > 0:
            cls = _lineup_cls(d['ab'], d['h'])
            lineup_rows_html += f'<td class="{cls}">{d["h"]}-{d["ab"]}</td>'
        elif d['bb'] > 0:
            lineup_rows_html += f'<td class="lo">BB×{d["bb"]}</td>'
        else:
            lineup_rows_html += f'<td class="lo">HBP×{d["hbp"]}</td>'
    lineup_rows_html += '</tr>\n'

_now_pt = datetime.now(ZoneInfo("America/Los_Angeles"))
GENERATED = _now_pt.strftime('%B %d, %Y, %-I:%M %p PT')
NUM_GAMES = len(GAMES)

# ── HTML ──────────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{theme.head('2026 SOLL 12U All-Stars')}
</head>
<body>

<div class="header">
{theme.THEME_TOGGLE_BUTTON}
  <h1>2026 SOLL 12U All-Stars</h1>
  <div class="sub">Updated {GENERATED}</div>
  <div class="record">
    <div class="stat"><div class="val">{wins}-{losses}</div><div class="lbl">Scrimmage Record</div></div>
    <div class="stat"><div class="val">{NUM_GAMES}</div><div class="lbl">Games</div></div>
    <div class="stat"><div class="val">{rs}</div><div class="lbl">Runs For</div></div>
    <div class="stat"><div class="val">{ra}</div><div class="lbl">Runs Against</div></div>
    <div class="stat"><div class="val">{pythag_str}</div><div class="lbl">Pythag W-L</div></div>
  </div>
</div>

<div class="section">

<!-- STANDARD BATTING -->
<div class="section-title">🥎 Batting — Standard</div>
<div class="tbl-wrap"><table>
<thead>
<tr>
  <th class="left">Player</th><th>GP</th><th>PA</th><th>AB</th><th>H</th>
  <th>2B</th><th>3B</th><th>HR</th><th>R</th><th>RBI</th>
  <th>BB</th><th>SO</th><th>SB</th><th>CS</th>
  <th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th>
</tr>
</thead><tbody>
"""

for p in sorted(players, key=lambda x: -x['batting']['ops']):
    b = p['batting']
    def cls(val, hi, med, flip=False):
        if flip:
            if val<=hi: return 'hi'
            if val<=med: return 'med'
            return 'bad'
        if val>=hi: return 'hi'
        if val>=med: return 'med'
        return 'lo'
    html += f"""<tr>
  <td class="name">{p['full']}</td><td>{b['gp']}</td>
  <td>{b['pa']}</td><td>{b['ab']}</td><td>{b['h']}</td>
  <td>{b['doubles']}</td><td>{b['triples']}</td><td>{b['hr']}</td>
  <td>{b['r']}</td><td>{b['rbi']}</td><td>{b['bb']}</td>
  <td class="{'bad' if b['so']>5 else ''}">{b['so']}</td>
  <td>{b['sb']}</td><td>{b['cs']}</td>
  <td class="{cls(b['avg'],.400,.300)}">{fmt(b['avg'])}</td>
  <td class="{cls(b['obp'],.500,.380)}">{fmt(b['obp'])}</td>
  <td class="{cls(b['slg'],.600,.450)}">{fmt(b['slg'])}</td>
  <td class="{cls(b['ops'],1.000,.800)}">{fmt(b['ops'])}</td>
</tr>"""

html += """</tbody></table></div>

<!-- ADVANCED BATTING -->
<div class="section-title">📊 Batting — Advanced</div>
<div class="tbl-wrap"><table>
<thead>
<tr class="th-group">
  <th class="left" colspan="1"></th>
  <th colspan="3">POWER</th>
  <th colspan="3">PLATE DISCIPLINE</th>
  <th colspan="3">RATE STATS</th>
  <th colspan="1">MISC</th>
</tr>
<tr>
  <th class="left">Player</th>
  <th>XBH</th><th>TB</th><th>ISO</th>
  <th>BB%</th><th>K%</th><th>HBP</th>
  <th>AVG</th><th>OBP</th><th>OPS</th>
  <th>SB%</th>
</tr>
</thead><tbody>
"""

for p in sorted(players, key=lambda x: -x['batting']['ops']):
    b = p['batting']
    html += f"""<tr>
  <td class="name">{p['full']}</td>
  <td>{b['xbh']}</td><td>{b['tb']}</td>
  <td class="{cls(b['iso'],.200,.100)}">{fmt(b['iso'])}</td>
  <td>{pct(b['bbpct'],0)}</td>
  <td class="{'bad' if b['kpct']>25 else ''}">{pct(b['kpct'],0)}</td>
  <td>{b['hbp']}</td>
  <td class="{cls(b['avg'],.400,.300)}">{fmt(b['avg'])}</td>
  <td class="{cls(b['obp'],.500,.380)}">{fmt(b['obp'])}</td>
  <td class="{cls(b['ops'],1.000,.800)}">{fmt(b['ops'])}</td>
  <td>{pct(b['sbpct'],0)}</td>
</tr>"""

html += f"""</tbody></table></div>

<!-- pQAB -->
<div class="section-title">✅ Quality At Bats (pQAB)</div>
<div style="background:var(--info-bg);border:1px solid var(--info-border);border-radius:8px;padding:12px 16px;margin-bottom:14px">
  <div style="font-weight:700;color:var(--info-heading);font-size:12px;margin-bottom:4px">ℹ️ Partial QAB Count — Data Limitations Apply</div>
  <div style="color:var(--text-muted);font-size:11px;line-height:1.6">
    <b style="color:var(--text-strong)">pQAB</b> counts plate appearances where the batter recorded a <b style="color:var(--text-strong)">Hit, Walk, HBP, RBI on an out, or a Hard-Hit Out</b>
    (line drive or hard-hit ground/fly ball, even when caught — from play-by-play logs where available).
    Criteria still <em>not</em> tracked: sac bunts, runner advancement to scoring position with &lt;2 outs, 8+ pitch ABs, 4+ pitches after an 0-2 count
    (none have occurred yet this season). True QAB% may still run slightly higher than shown.
    Per baseballmode.com: average is 40–50% at 12U travel ball; 55%+ is elite.
  </div>
</div>
<div class="tbl-wrap"><table>
<thead>
<tr class="th-group">
  <th class="left" colspan="1"></th>
  <th colspan="5">QUALIFYING OUTCOMES (TRACKED)</th>
  <th colspan="2">pQAB</th>
</tr>
<tr>
  <th class="left">Player</th>
  <th>PA</th><th>H</th><th>BB</th><th>HBP</th><th>HH Out</th>
  <th>pQAB</th><th>pQAB%</th>
</tr>
</thead><tbody>
{pqab_rows_html}
</tbody></table></div>
<!-- END pQAB -->

<!-- LINEUP POSITION HEATMAP -->
<div class="section-title">🔢 Performance by Batting Order Position</div>
<div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:10px 16px;margin-bottom:14px;color:var(--text-muted);font-size:11px;line-height:1.6">
  H-AB totals across all games when a player batted in that lineup spot. Dashes mean the player never batted there.
</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th>
  {lineup_header_html}
</tr></thead><tbody>
{lineup_rows_html}
</tbody></table></div>
<!-- END LINEUP HEATMAP -->

<!-- PITCHING -->
<div class="section-title">⚾ Pitching</div>
<div class="tbl-wrap"><table>
<thead>
<tr class="th-group">
  <th class="left" colspan="2"></th>
  <th colspan="8">STATS</th>
  <th colspan="7">RATES</th>
  <th colspan="2">PITCHING DATA</th>
</tr>
<tr>
  <th class="left">Player</th><th>App</th>
  <th>IP</th><th>H</th><th>R</th><th>ER</th><th>HR</th><th>BB</th><th>K</th><th>HBP</th>
  <th>ERA</th><th>WHIP</th><th>FIP</th><th>K/IP</th><th>K/BB</th><th>BAA</th><th>Strike%</th>
  <th>Total P</th><th>Last PC</th>
</tr>
</thead><tbody>
"""

pit_players = [(p, p['pitching']) for p in players if p['pitching']]
pit_players.sort(key=lambda x: -x[1]['ip_d'])
for p, pl in pit_players:
    def pcls(val, good, ok, flip=False):
        if flip:
            if val<=good: return 'hi'
            if val<=ok:   return 'med'
            return 'bad'
        if val>=good: return 'hi'
        if val>=ok:   return 'med'
        return 'lo'
    kbb_s = fmt(pl['kbb'],2) if pl['kbb'] else '—'
    html += f"""<tr>
  <td class="name">{p['full']}</td><td>{pl['apps']}</td>
  <td>{pl['ip']}</td><td>{pl['h']}</td><td>{pl['r']}</td><td>{pl['er']}</td><td>{pl['hr']}</td>
  <td>{pl['bb']}</td>
  <td class="{pcls(pl['kip'],1.5,1.0)}">{pl['k']}</td>
  <td>{pl['hbp']}</td>
  <td class="{pcls(pl['era'],3.0,6.0,flip=True)}">{fmt_lz(pl['era'],2)}</td>
  <td class="{pcls(pl['whip'],1.2,1.8,flip=True)}">{fmt_lz(pl['whip'],2)}</td>
  <td class="{pcls(pl['fip'],3.5,5.5,flip=True)}">{fmt_lz(pl['fip'],2)}</td>
  <td class="{pcls(pl['kip'],1.5,1.0)}">{fmt(pl['kip'],2)}</td>
  <td class="{pcls(float(pl['kbb']) if pl['kbb'] else 0,3.0,1.5)}">{kbb_s}</td>
  <td class="{pcls(pl['baa'],.200,.300,flip=True)}">{fmt(pl['baa'])}</td>
  <td class="{pcls(pl['spct'],.65,.58)}">{pl['spct']:.1%}</td>
  <td>{pl['pitches']}</td>
  <td>{pl['last_pc']}p {'· ' + pl['last_date'] if pl['last_date'] else ''}</td>
</tr>"""

html += """</tbody></table></div>

<!-- PITCHING PER-GAME SPLITS -->
<div class="section-title">📅 Pitching — Per-Game Splits</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th>
"""

for game_id, date_str in game_ids:
    gi = game_log_by_id.get(game_id, {})
    opp = gi.get('opp', 'Game')
    res = gi.get('result', '')
    score = gi.get('score', '')
    res_color = 'var(--green)' if res=='W' else 'var(--red)' if res=='L' else 'var(--text-muted)'
    g_label = game_label_suffix[game_id]
    html += f'<th style="min-width:90px"><div style="color:{res_color};font-weight:700">{res} {score}</div><div style="font-size:10px;color:var(--text-dim)">{opp}</div><div style="font-size:10px;color:var(--text-faint)">{date_str}{g_label}</div></th>'

html += """</tr></thead><tbody>
"""

for p, _ in pit_players:
    html += f'<tr><td class="name">{p["full"]}</td>'
    for g in p['per_game_pitch']:
        if not g['pitched']:
            html += '<td class="dnp">—</td>'
        else:
            er_cls = 'hi' if g['er']==0 else 'med' if g['er']<=1 else 'bad'
            line2 = ' '.join(filter(None, [f'{g["h"]}H' if g["h"] else '', f'{g["r"]}R' if g["r"] else '', f'{g["er"]}ER' if g["er"] else '']))
            line3 = ' '.join(filter(None, [f'{g["bb"]}BB' if g["bb"] else '', f'{g["so"]}K' if g["so"] else '', f'{g["pitches"]}P' if g["pitches"] else '']))
            html += f'<td><div class="{er_cls}" style="font-weight:700;font-size:13px">{g["ip"]} IP</div><div style="font-size:10px;color:var(--text-dim)">{line2 or "—"}</div><div style="font-size:10px;color:var(--text-faint)">{line3}</div></td>'
    html += '</tr>'

html += """</tbody></table></div>

<!-- PITCH COUNT LOG -->
<div class="section-title">📋 Pitch Count & Availability</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th><th>Status</th>
  <th>Last Outing</th><th>Last Pitches</th><th>Rest Required</th>
  <th>Season IP</th><th>Season Pitches</th>
</tr></thead><tbody>
"""

for p in sorted(players, key=lambda x:(
    0 if x['avail']=='available' else 1 if x['avail']=='soon' else 2, x['full'])):
    pl = p['pitching']
    if pl:
        rest = rest_days_required(pl['last_pc'])
        rest_s = f"{rest}d" if rest > 0 else "None"
        elig_s = p['elig'] if p['elig'] else "Now"
    else:
        rest_s = '—'; elig_s = '—'
    html += f"""<tr>
  <td class="name">{p['full']}</td>
  <td>{avail_badge(p['avail'], p['elig'])}</td>
  <td>{'· '.join([pl['last_date']]) if pl and pl['last_date'] else '—'}</td>
  <td>{pl['last_pc'] if pl else '—'}</td>
  <td>{rest_s}</td>
  <td>{pl['ip'] if pl else '—'}</td>
  <td>{pl['pitches'] if pl else '—'}</td>
</tr>"""

html += """</tbody></table></div>

<!-- FIELDING -->
<div class="section-title">🧤 Fielding</div>
<div style="background:var(--warn-bg);border:1px solid var(--warn-border);border-radius:8px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;gap:12px">
  <span style="font-size:22px">🚧</span>
  <div>
    <div style="font-weight:700;color:var(--warn-heading);font-size:13px">Partial Stats — From Play-by-Play</div>
    <div style="color:var(--warn-text);font-size:12px;margin-top:2px">PO, A, and DP are pulled from play-by-play descriptions and only counted when a SOLL fielder is named. Many routine plays (e.g. unassisted putouts at first, strikeout catcher putouts) don't name a fielder and aren't counted — so PO/A/DP are minimums, not official totals. Errors (E) are accurate, from game files.</div>
  </div>
</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th><th>GP</th><th>PO</th><th>A</th><th>E</th><th>DP</th><th>FLD%</th>
</tr></thead><tbody>
"""

for p in sorted(players, key=lambda x: x['full']):
    b = p['batting']
    f = p['field']
    e_cls = 'bad' if b['e'] > 2 else 'med' if b['e'] > 0 else 'dim'
    pct_cls = 'dim' if f['pct'] is None else ('hi' if f['pct']>=.950 else 'med' if f['pct']>=.900 else 'bad')
    pct_s = fmt(f['pct']) if f['pct'] is not None else '—'
    html += f"""<tr>
  <td class="name">{p['full']}</td>
  <td>{b['gp']}</td>
  <td class="{'dim' if f['po']==0 else ''}">{f['po']}</td>
  <td class="{'dim' if f['a']==0 else ''}">{f['a']}</td>
  <td class="{e_cls}">{b['e']}</td>
  <td class="{'dim' if f['dp']==0 else ''}">{f['dp']}</td>
  <td class="{pct_cls}">{pct_s}</td>
</tr>"""

html += """</tbody></table></div>

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
      <span class="heat" style="font-size:22px">{p['heat_icon']}</span>
      <div><div style="font-size:11px;color:var(--text-dim)">L3 OPS</div>
        <div style="font-size:18px;font-weight:800;color:var(--accent)">{l3_ops_s}</div></div>
      <div style="margin-left:auto;text-align:right">
        <div style="font-size:11px;color:{p['heat_color']};font-weight:700;letter-spacing:1px">{p['heat_label']}</div>
        <div style="font-size:11px;color:var(--text-dim);margin-top:2px">Season {fmt(p['batting']['ops'])}</div></div>
    </div>
    <div class="l3-stats">
      <div class="l3-stat"><div class="l3-val">{l3_avg_s}</div><div class="l3-lbl">AVG</div></div>
      <div class="l3-stat"><div class="l3-val">{p['l3_r']}</div><div class="l3-lbl">R</div></div>
      <div class="l3-stat"><div class="l3-val">{p['l3_rbi']}</div><div class="l3-lbl">RBI</div></div>
    </div>
  </div>"""

html += """
</div>

<!-- PER-GAME SPLITS -->
<div class="section-title">📅 Per-Game Splits</div>
<div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Player</th>
"""

for game_id, date_str in game_ids:
    gi = game_log_by_id.get(game_id, {})
    opp = gi.get('opp', 'Game')
    res = gi.get('result', '')
    score = gi.get('score', '')
    res_color = 'var(--green)' if res=='W' else 'var(--red)' if res=='L' else 'var(--text-muted)'
    g_label = game_label_suffix[game_id]
    html += f'<th style="min-width:90px"><div style="color:{res_color};font-weight:700">{res} {score}</div><div style="font-size:10px;color:var(--text-dim)">{opp}</div><div style="font-size:10px;color:var(--text-faint)">{date_str}{g_label}</div></th>'

html += """</tr></thead><tbody>
"""

for p in sorted(players, key=lambda x: x['full']):
    html += f'<tr><td class="name">{p["full"]}</td>'
    for g in p['per_game']:
        if g['dnp']:
            html += '<td class="dnp">DNP</td>'
        else:
            avg_cls = 'hi' if (g['avg'] or 0)>=.400 else 'med' if (g['avg'] or 0)>=.300 else 'lo'
            hab_s = f'{g["h"]}-{g["ab"]}' if g['ab'] > 0 else f'BB×{g["bb"]}' if g['bb'] > 0 else '—'
            line2 = ' '.join(filter(None, [f'{g["r"]}R' if g["r"] else '', f'{g["rbi"]}RBI' if g["rbi"] else '', f'{g["bb"]}BB' if g["bb"] else '', f'{g["hbp"]}HBP' if g["hbp"] else '']))
            extras = ' '.join(filter(None, [f'{g["sb"]}SB' if g["sb"] else '', f'{g["so"]}K' if g["so"] else '']))
            html += f'<td><div class="{avg_cls}" style="font-weight:700;font-size:13px">{hab_s}</div><div style="font-size:10px;color:var(--text-dim)">{line2}</div><div style="font-size:10px;color:var(--text-faint)">{extras}</div></td>'
    html += '</tr>'

html += """</tbody></table></div>

<!-- GAME LOG -->
<div class="section-title">📋 Game Log</div>
"""

if not GAMES:
    html += '<div class="no-games">No games recorded yet.</div>'
else:
    for g in reversed(GAMES):
        us   = g['away_score'] if g['away']=='SOLL' else g['home_score']
        them = g['home_score'] if g['away']=='SOLL' else g['away_score']
        opp  = g['home'] if g['away']=='SOLL' else g['away']
        res  = 'W' if g['winner']=='SOLL' else 'L'
        rnd  = g.get('round',''); field = g.get('field','')
        gid  = game_id_by_game.get(id(g))
        tag  = 'a' if gid else 'div'
        href = f' href="games/{gid}.html"' if gid else ''
        arrow = '<span class="arrow">→</span>' if gid else ''
        html += f"""<{tag} class="game-row"{href}>
  <span class="result {res}">{res}</span>
  <span class="score">{us}–{them}</span>
  <span class="opp">vs {opp}{' · ' + field if field else ''}</span>
  <span>{g['date']}</span>
  {'<span class="round">' + rnd + '</span>' if rnd else ''}
  {arrow}
</{tag}>"""

html += f"""
</div>
<div class="footer">2026 SOLL 12U All-Stars · Generated {GENERATED} · {NUM_GAMES} games</div>
</body></html>"""

out_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard.html')
with open(out_path, 'w') as f:
    f.write(html)

print(f"✅  Dashboard written to: {os.path.abspath(out_path)}")
print(f"    Games: {NUM_GAMES}  |  Record: {wins}-{losses}  |  Players: {len(ROSTER)}")
