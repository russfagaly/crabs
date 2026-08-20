#!/usr/bin/env python3
"""
generate.py — rebuild pitching/index.html from the bb-2026 per-game files.

Why this exists
---------------
This page used to be a hand-authored HTML file with no source anywhere. When a
one-word change was needed it had to be decrypted out of the published page to
edit. Generating it instead means:
  * the source of truth is the bb-2026 game files, not a frozen artifact;
  * build_hub.py rewrites it as fresh plaintext every run, so publish.sh always
    encrypts plaintext exactly once (the double-encryption guard never has to
    save us);
  * regenerating picks up any correction made upstream.

If the bb-2026 repo is not present this exits WITHOUT touching index.html, so a
machine without it simply keeps the last published copy.

ERA basis
---------
9 innings, matching Stats/pipeline/compile_html.py and the league workbook
(whose own ERA column is 9-based: 23 ER x 9 / 26 IP = 7.96). The earlier version
of this page used a 6-inning basis, which contradicted the league's own numbers.
K/6 and BB/6 stay on 6 innings, a regulation Little League game.
"""
import os, sys, html
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
BB = os.environ.get("BB2026_DIR", os.path.join(os.path.dirname(os.path.dirname(HERE)), "bb-2026"))
GAMES = os.path.join(BB, "Stats", "games")
SEASON = os.path.join(BB, "Stats", "data", "season_2026.json")
PIPELINE = os.path.join(BB, "Stats", "pipeline")
OUT = os.path.join(HERE, "index.html")

# (short name in game files, team, full display name, jersey)
ROSTER = [
    ("Kaleo P",  "Marlins",   "Kaleo Pontemayor", 10),
    ("Mayer H",  "Marlins",   "Mayer Hemberg",     5),
    ("Roland M", "Yankees",   "Roland Meyer",     99),
    ("Samuel G", "Padres",    "Samuel Gilmore",    7),
    ("Adrien R", "White Sox", "Adrien Romero",     6),
    ("Carter F", "Astros",    "Carter Flores",    24),
    ("RJ F",     "Padres",    "RJ Fagaly",        22),
    ("Orion M",  "Padres",    "Orion Mitchell",   13),
]

if not os.path.isdir(GAMES):
    print(f"  pitching: {GAMES} not found — leaving index.html untouched")
    sys.exit(0)

sys.path.insert(0, PIPELINE)
try:
    import last4
except ImportError:
    print("  pitching: bb-2026 last4.py not importable — leaving index.html untouched")
    sys.exit(0)


def ip_to_dec(s):
    w, f = str(s).split('.')
    return int(w) + int(f) / 3


def dec_to_ip(d):
    w = int(d)
    return f"{w}.{round((d - w) * 3)}"


apps, warnings = last4.load_appearances(GAMES, SEASON, ip_to_dec)
built = {(p['team'], p['display']): p for p in last4.build(apps, dec_to_ip)}
for w in warnings:
    print(f"  pitching WARNING: {w}")

rows = []
for short, team, full, jersey in ROSTER:
    p = built.get((team, short))
    if not p:
        print(f"  pitching WARNING: {full} not found as ({team}, {short}) — omitted")
        continue
    rows.append((full, jersey, p))
rows.sort(key=lambda r: -(r[2]['last_n']['spct'] or 0))

E = html.escape
def f(v, n=2): return "&mdash;" if v is None else f"{v:.{n}f}"
def pc(v, n=1): return "&mdash;" if v is None else f"{v*100:.{n}f}%"

# ── comparison table ─────────────────────────────────────────────────────────
comp = []
for full, jersey, p in rows:
    t = p['last_n']
    few = f' <span class=warn2>{p["total_apps"]} app</span>' if p['total_apps'] < 4 else ''
    comp.append(
        f"<tr><td>{E(full)} <span class=sub2>{E(p['team'])}</span>{few}</td>"
        f"<td class=n>{t['ip']}</td><td class=n>{t['bf']}</td><td class=n>{t['pitches']}</td>"
        f"<td class='n hi'>{pc(t['spct'])}</td>"
        f"<td class=n>{f(t['pitches']/t['ip_dec'],1) if t['ip_dec'] else '&mdash;'}</td>"
        f"<td class=n>{f(t['pitches']/t['bf'],1) if t['bf'] else '&mdash;'}</td>"
        f"<td class='n k'>{t['so']}</td><td class='n bbc'>{t['bb']}</td>"
        f"<td class=n>{f(t['kbb'])}</td><td class=n>{f(t['whip'])}</td>"
        f"<td class=n>{f(t['era'])}</td>"
        f"<td class=n>{f(t['h']/(t['bf']-t['bb']-t['hbp']),3) if (t['bf']-t['bb']-t['hbp'])>0 else '&mdash;'}</td></tr>")

# ── per-pitcher cards ────────────────────────────────────────────────────────
cards = []
for full, jersey, p in rows:
    t, s = p['last_n'], p['season']
    a0, a1 = p['appearances'][0]['date'], p['appearances'][-1]['date']
    meta = (f"Last {len(p['appearances'])} of {p['total_apps']} appearances &middot; "
            f"{a0[5:].replace('-','/')} &ndash; {a1[5:].replace('-','/')}")
    tiles = "".join(
        f"<div class='tile{c}'><div class=tv>{v}</div><div class=tk>{k}</div></div>"
        for k, v, c in [
            ("IP", t['ip'], ''), ("Batters faced", t['bf'], ''), ("Pitches", t['pitches'], ''),
            ("Strikes", t['strikes'], ''), ("Strike %", pc(t['spct']), ''),
            ("P / IP", f(t['pitches']/t['ip_dec'],1) if t['ip_dec'] else '&mdash;', ''),
            ("P / BF", f(t['pitches']/t['bf'],1) if t['bf'] else '&mdash;', ''),
            ("K", t['so'], ' acc'), ("BB", t['bb'], ' acc'),
            ("K / BB", f(t['kbb']), ''), ("WHIP", f(t['whip']), ''), ("ERA", f(t['era']), '')])
    log = []
    for a in p['appearances']:
        ha = 'home' if a['home'] else 'away'
        res = f"{a['result']} {a['us']}&ndash;{a['them']}" if a['result'] else '&mdash;'
        log.append(
            f"<tr><td class=d>{a['date'][5:].replace('-','/')}</td>"
            f"<td class=opp>{E(a['opp'])}</td><td class=res>{res}</td>"
            f"<td class=n>{a['ip']}</td><td class=n>{a['bf']}</td><td class=n>{a['pitches']}</td>"
            f"<td class=n>{a['strikes']}</td><td class='n sp'>{pc(a['spct_g'],0)}</td>"
            f"<td class=n>{a['h']}</td><td class=n>{a['r']}</td><td class=n>{a['er']}</td>"
            f"<td class='n bbc'>{a['bb']}</td><td class='n k'>{a['so']}</td>"
            f"<td class=n>{a['hbp']}</td>"
            f"<td class=n>{a['rest'] if a['rest'] is not None else '&mdash;'}</td></tr>")
    log.append(
        f"<tr class=tot><td colspan=3>Total</td><td class=n>{t['ip']}</td><td class=n>{t['bf']}</td>"
        f"<td class=n>{t['pitches']}</td><td class=n>{t['strikes']}</td>"
        f"<td class='n sp'>{pc(t['spct'],0)}</td><td class=n>{t['h']}</td><td class=n>{t['r']}</td>"
        f"<td class=n>{t['er']}</td><td class='n bbc'>{t['bb']}</td><td class='n k'>{t['so']}</td>"
        f"<td class=n>{t['hbp']}</td><td class=n></td></tr>")
    flag = (f"<div class=flag>Only {p['total_apps']} appearance(s) on file &mdash; "
            f"this card shows all of them.</div>") if p['total_apps'] < 4 else ""
    cards.append(f"""<section class=card>
<h2>{E(full)} <span class=sub>#{jersey} &middot; {E(p['team'])}</span></h2>
<div class=meta>{meta}</div>{flag}
<div class=tiles>{tiles}</div>
<div class=szn>Season: <b>{s['g']}</b> appearances &middot; <b>{s['ip']}</b> IP &middot;
ERA <b>{f(s['era'])}</b> &middot; WHIP <b>{f(s['whip'])}</b> &middot; K <b>{s['so']}</b> &middot;
BB <b>{s['bb']}</b> &middot; Strike% <b>{pc(s['spct'])}</b></div>
<table class=log><thead><tr><th>Date</th><th>Opponent</th><th>Result</th><th class=n>IP</th>
<th class=n>BF</th><th class=n>P</th><th class=n>S</th><th class=n>S%</th><th class=n>H</th>
<th class=n>R</th><th class=n>ER</th><th class=n>BB</th><th class=n>K</th><th class=n>HBP</th>
<th class=n>Rest</th></tr></thead><tbody>{''.join(log)}</tbody></table></section>""")

season_end = max(a['date'] for a in apps)
n_games = len({(a['date'], a['team']) for a in apps})
doc = f"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Last Four Pitching Appearances &mdash; Spring Season</title>
<style>
:root{{--bg:#faf9f7;--card:#fff;--ink:#1a1a18;--mut:#6b6963;--line:#e5e2dc;--acc:#1D9E75;--warn:#B4560F}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:32px 20px 64px}}
h1{{font-size:26px;margin:0 0 6px;letter-spacing:-.02em}}
.lede{{color:var(--mut);margin:0 0 22px;max-width:72ch}}
.notice{{background:#eef7f3;border:1px solid #cfe8de;border-left:3px solid var(--acc);border-radius:8px;padding:14px 16px;margin:0 0 26px;font-size:13.5px;color:#2d4a40}}
.notice b{{color:#1d3830}} .notice ul{{margin:8px 0 0;padding-left:18px}} .notice li{{margin:3px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px 20px 8px;margin:0 0 20px}}
h2{{font-size:19px;margin:0 0 2px;letter-spacing:-.01em}}
.sub{{font-weight:400;color:var(--mut);font-size:13px;margin-left:6px}}
.sub2{{color:var(--mut);font-size:12px}}
.warn2{{background:#fdf0e2;color:#94500d;font-size:10.5px;padding:2px 7px;border-radius:20px;font-weight:600;margin-left:4px}}
.meta{{color:var(--mut);font-size:12.5px;margin-bottom:14px}}
.flag{{background:#fdf6ec;border-radius:6px;padding:8px 11px;font-size:12.5px;color:#6b5330;margin-bottom:14px}}
.szn{{background:#f6f5f2;border-radius:8px;padding:9px 12px;font-size:12.5px;color:#4a4844;margin:0 0 14px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(86px,1fr));gap:8px;margin-bottom:14px}}
.tile{{background:#f6f5f2;border-radius:8px;padding:10px 8px;text-align:center}}
.tile.acc{{background:#e9f4f0}}
.tv{{font-variant-numeric:tabular-nums;font-size:17px;font-weight:650;letter-spacing:-.02em}}
.tk{{font-size:10.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}}
th{{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);font-weight:600;padding:6px 6px;border-bottom:1px solid var(--line)}}
td{{padding:7px 6px;border-bottom:1px solid #f2f0eb}}
td.n,th.n{{text-align:right}}
td.d{{white-space:nowrap;color:var(--mut)}} td.opp{{white-space:nowrap}} td.res{{color:var(--mut);white-space:nowrap}}
td.k{{font-weight:650;color:#0f6b4f}} td.bbc{{font-weight:600;color:#94500d}} td.sp{{font-weight:600}}
tr.tot td{{border-top:2px solid var(--line);border-bottom:none;font-weight:650;background:#fbfaf8}}
.comp{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;margin:0 0 20px;overflow-x:auto}}
.comp td.hi{{font-weight:650;color:var(--acc)}}
.foot{{color:var(--mut);font-size:12.5px;margin-top:26px;line-height:1.6}}
@media(max-width:720px){{.card{{padding:16px 12px 4px}}table{{font-size:12px}}}}
</style></head><body><div class=wrap>
<h1>Last Four Pitching Appearances</h1>
<p class=lede>Alameda Little League Majors &mdash; <b>full spring season including playoffs</b>.
Each pitcher's own last four outings, not the team's last four games.</p>

<div class=notice><b>Now covering the complete season.</b>
<ul>
<li>All <b>{n_games} team-games</b> across the season are on file, through <b>{season_end[5:].replace('-','/')}</b>,
including the playoff run and the championship game.</li>
<li>An earlier version of this page stopped at 04/19 because the later per-game
files were missing. They were recovered from a Drive backup, so every card below
now reflects each pitcher's genuinely most recent four outings.</li>
</ul></div>

<div class=comp><h2 style="margin-bottom:12px">Side by side <span class=sub>totals over the window, sorted by strike %</span></h2>
<table><thead><tr><th>Pitcher</th><th class=n>IP</th><th class=n>BF</th><th class=n>Pitches</th><th class=n>Strike %</th>
<th class=n>P/IP</th><th class=n>P/BF</th><th class=n>K</th><th class=n>BB</th><th class=n>K/BB</th>
<th class=n>WHIP</th><th class=n>ERA</th><th class=n>BAA</th></tr></thead>
<tbody>{''.join(comp)}</tbody></table></div>

{''.join(cards)}

<div class=foot>Source: per-game files in <code>bb-2026/Stats/games/</code>, generated from
<code>crabs-site/pitching/generate.py</code>. Strike % = strikes &divide; total pitches.
ERA is on a 9-inning basis, matching the league workbook and the main Majors stats site;
K/6 and BB/6 elsewhere use a 6-inning regulation game. BAA = H &divide; (BF &minus; BB &minus; HBP).
Rest = calendar days since that pitcher's previous outing.
Generated {date.today().strftime('%m/%d/%Y')}.</div>
</div></body></html>"""

open(OUT, 'w', encoding='utf-8').write(doc)
print(f"  pitching: rebuilt {OUT} ({len(doc):,} bytes, {len(rows)} pitchers, season through {season_end})")
