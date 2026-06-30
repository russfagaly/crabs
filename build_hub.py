#!/usr/bin/env python3
# build_hub.py — regenerate every team, inject the switcher, rebuild the hub
# landing (team cards + Scouting Reports section). Run from repo root.
import glob, os, subprocess, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = "hub-switcher-v1"

# (slug, switcher_label, card_title, card_meta, accent, record_token)
TEAMS = [
    ("alameda_districts", "Alameda Crabs",    "Alameda Crabs",       "12U All-Stars · District tournament", "#f97316", "Alameda"),
    ("alameda",           "Crabs Scrimmages", "Crabs Scrimmages",    "12U All-Stars · 9 scrimmages",        "#fb7185", "Alameda"),
    ("noll",              "NOLL",             "NOLL",                "North Oakland 12U · Districts",        "#22d3ee", "NOLL"),
    ("lightning",         "Lightning",        "Lafayette Lightning", "12U · 9 games · scouting",             "#fbbf24", "Lightning"),
    ("soll",              "SOLL",             "SOLL",                "South Oakland 12U · Districts",        "#34d399", "SOLL"),
]

# Scouting reports (newest first). Drop the HTML in scouting/ then add a line.
# (filename_in_scouting, title, subtitle, date_label)
REPORTS = [
    ("2026-07-01_crabs-vs-soll.html", "Crabs vs SOLL", "District tournament · rematch scouting", "Jul 1, 2026"),
    ("2026-06-29_crabs-vs-noll.html", "Crabs vs NOLL", "District tournament · pre-game scouting", "Jun 29, 2026"),
]

def sh(cmd, cwd): return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)

def record(slug):
    p = os.path.join(ROOT, slug, "pipeline", "results.py")
    spec = importlib.util.spec_from_file_location("r_"+slug, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    r = m.get_record(); w, l = r[0], r[1]; t = r[2] if len(r) > 2 else 0
    return f"{w}–{l}" + (f"–{t}" if t else "")

def nav(active):
    links = ['<a href="../" style="color:#8b949e;text-decoration:none;padding:6px 11px;border-radius:6px">&#127968; Home</a>']
    for slug,label,*_ in TEAMS:
        st = "background:#238636;color:#fff" if slug==active else "color:#c9d1d9;background:#21262d"
        links.append(f'<a href="../{slug}/" style="text-decoration:none;padding:6px 11px;border-radius:6px;{st}">{label}</a>')
    return (f'<div class="{MARK}" style="position:sticky;top:0;z-index:99999;background:#0d1117;'
            f'border-bottom:1px solid #30363d;display:flex;justify-content:center;gap:4px;padding:8px 12px;'
            f'flex-wrap:wrap;align-items:center;font:600 13px/1 -apple-system,system-ui,sans-serif">'
            + "".join(links) + '</div>')

def inject(path, active):
    html = open(path, encoding="utf-8").read()
    if MARK in html: return
    i = html.lower().find("<body"); j = html.find(">", i)+1
    open(path,"w",encoding="utf-8").write(html[:j] + "\n" + nav(active) + html[j:])

# 1. regenerate each team + inject switcher
recs = {}
for slug,label,title,meta,accent,token in TEAMS:
    d = os.path.join(ROOT, slug)
    sh("python3 pipeline/generate_dashboard.py", d)
    sh("python3 pipeline/generate_game_pages.py", d)
    if os.path.exists(os.path.join(d,"pipeline","generate_scouting.py")):
        sh("python3 pipeline/generate_scouting.py", d)
    sh("cp dashboard.html index.html", d)
    for fn in ("index.html","dashboard.html","scouting.html"):
        fp = os.path.join(d, fn)
        if os.path.exists(fp): inject(fp, slug)
    recs[slug] = record(slug)
    print(f"  {slug}: {recs[slug]}")

# 2. inject switcher into scouting report pages (no active team)
for fp in glob.glob(os.path.join(ROOT,"scouting","*.html")):
    inject(fp, "")
print(f"  scouting reports: {len(REPORTS)}")

# 3. build hub landing
cards = ""
for slug,label,title,meta,accent,token in TEAMS:
    cards += f'''  <a class="card" style="--accent:{accent}" href="./{slug}/">
    <div class="team"><span class="dot"></span>{title}</div>
    <div class="meta">{meta}</div>
    <div class="rec">{recs[slug]}</div><div class="reclbl">Record</div>
    <div class="go">View dashboard &rarr;</div>
  </a>\n'''

reports_html = ""
if REPORTS:
    rows = ""
    for fn,title,sub,dt in REPORTS:
        rows += f'''    <a class="report" href="./scouting/{fn}">
      <div class="rdate">{dt}</div>
      <div class="rmain"><div class="rtitle">{title}</div><div class="rsub">{sub}</div></div>
      <div class="rarrow">&rarr;</div>
    </a>\n'''
    reports_html = f'''<section class="reports-wrap">
  <h2 class="shead">&#128270; Scouting Reports</h2>
  <div class="reports">
{rows}  </div>
</section>'''

hub = f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>2026 All-Stars Hub</title>
<style>
 :root{{color-scheme:dark}} *{{box-sizing:border-box}}
 body{{margin:0;background:#0d1117;color:#e6edf3;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:48px 20px}}
 header{{text-align:center;margin-bottom:40px}} h1{{font-size:32px;margin:0 0 6px;letter-spacing:-.5px}} .sub{{color:#8b949e;font-size:15px}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;width:100%;max-width:920px}}
 a.card{{display:block;text-decoration:none;color:inherit;background:#161b22;border:1px solid #30363d;border-radius:14px;padding:24px;transition:border-color .15s,transform .15s}}
 a.card:hover{{transform:translateY(-3px);border-color:var(--accent)}}
 .team{{font-size:21px;font-weight:700;margin:0 0 4px;display:flex;align-items:center;gap:9px}}
 .dot{{width:11px;height:11px;border-radius:50%;background:var(--accent)}}
 .meta{{color:#8b949e;font-size:14px;margin-bottom:14px}} .rec{{font-size:30px;font-weight:800;letter-spacing:-1px}}
 .reclbl{{color:#8b949e;font-size:12px;text-transform:uppercase;letter-spacing:.6px}} .go{{margin-top:14px;color:#58a6ff;font-size:14px;font-weight:600}}
 .reports-wrap{{width:100%;max-width:920px;margin-top:40px}}
 .shead{{font-size:18px;margin:0 0 14px;color:#e6edf3}}
 .reports{{display:flex;flex-direction:column;gap:10px}}
 a.report{{display:flex;align-items:center;gap:16px;text-decoration:none;color:inherit;background:#161b22;border:1px solid #30363d;border-radius:12px;padding:14px 18px;transition:border-color .15s}}
 a.report:hover{{border-color:#f97316}}
 .rdate{{flex:none;font-size:12px;color:#8b949e;width:92px}}
 .rmain{{flex:1}} .rtitle{{font-weight:700;font-size:16px}} .rsub{{color:#8b949e;font-size:13px}}
 .rarrow{{color:#58a6ff;font-weight:700;font-size:18px}}
 footer{{margin-top:48px;color:#6e7681;font-size:13px;text-align:center}}
</style></head><body>
<header><h1>2026 All-Stars Hub</h1><div class="sub">Hitting &amp; pitching dashboards &middot; 12U All-Star season</div></header>
<div class="grid">
{cards}</div>
{reports_html}
<footer>2026 All-Stars Hub &middot; russfagaly.github.io/crabs</footer>
</body></html>'''
open(os.path.join(ROOT,"index.html"),"w",encoding="utf-8").write(hub)
print(f"hub landing rebuilt: {len(TEAMS)} tabs, {len(REPORTS)} scouting report(s)")
