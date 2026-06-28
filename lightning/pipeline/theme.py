# theme.py — Lafayette Lightning
# Shared dark/light theme (CSS variables + toggle script + toggle button)
# used by generate_dashboard.py and generate_game_pages.py.
#
# Color scheme: electric yellow + dark stormy navy

CSS_BLOCK = """<style>
:root{
  --bg:#0d1520; --text:#d1dce8; --text-strong:#e8f0f8;
  --text-muted:#8fa8c0; --text-dim:#5a7a96; --text-faint:#3d5a72; --text-faintest:#2a3d50;
  --border:#1e3050; --border-soft:#152640;
  --surface:#131e2b; --surface-2:#0f1a25; --surface-3:#0d1824; --surface-deep:#0d1520;
  --th-group-bg:#0a1420;
  --row-hover:#1e305088; --row-hover-name:#1a2e48;
  --accent:#fbbf24; --green:#4ade80; --yellow:#fbbf24; --red:#f87171;
  --header-grad-1:#1a2f3a; --header-grad-2:#0d1520;
  --info-bg:#1a2c1a; --info-border:#2d5a2d; --info-heading:#86efac;
  --warn-bg:#2a1f0a; --warn-border:#92400e; --warn-heading:#fbbf24; --warn-text:#d97706;
}
[data-theme="light"]{
  --bg:#f0f4f8; --text:#1e2d3d; --text-strong:#0d1a26;
  --text-muted:#5a7a96; --text-dim:#8fa8c0; --text-faint:#a0b8cc; --text-faintest:#c8d8e4;
  --border:#b8d0e0; --border-soft:#d4e4f0;
  --surface:#ffffff; --surface-2:#f6f9fc; --surface-3:#eef3f8; --surface-deep:#e4edf5;
  --th-group-bg:#dceaf4;
  --row-hover:#b8d0e055; --row-hover-name:#fff3c4;
  --accent:#d97706; --green:#16a34a; --yellow:#d97706; --red:#dc2626;
  --header-grad-1:#d4e8f5; --header-grad-2:#f0f4f8;
  --info-bg:#f0fdf4; --info-border:#bbf7d0; --info-heading:#15803d;
  --warn-bg:#fffbeb; --warn-border:#fde68a; --warn-heading:#b45309; --warn-text:#92400e;
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,Arial,sans-serif;font-size:14px;line-height:1.4;transition:background .15s,color .15s}
.header{position:relative;background:linear-gradient(135deg,var(--header-grad-1),var(--header-grad-2));padding:20px 16px;text-align:center;border-bottom:2px solid var(--border)}
.header h1{font-size:clamp(17px,4vw,24px);font-weight:800;color:var(--accent);letter-spacing:1px;text-shadow:0 0 20px rgba(251,191,36,.35)}
.header h1 a{color:inherit;text-decoration:none}
.header .sub{font-size:clamp(11px,2.5vw,13px);color:var(--text-muted);margin-top:4px}
.record{display:flex;flex-wrap:wrap;gap:16px 24px;justify-content:center;margin-top:14px}
.record .stat{text-align:center;min-width:60px}
.record .val{font-size:clamp(20px,5vw,28px);font-weight:800;color:var(--accent)}
.record .lbl{font-size:10px;color:var(--text-dim);text-transform:uppercase;letter-spacing:1px}
#theme-toggle{position:absolute;top:12px;right:12px;background:var(--surface);border:1px solid var(--border);
  border-radius:20px;width:36px;height:36px;font-size:16px;cursor:pointer;display:flex;align-items:center;
  justify-content:center;color:var(--text)}
#theme-toggle .sun{display:none}
[data-theme="light"] #theme-toggle .sun{display:inline}
[data-theme="light"] #theme-toggle .moon{display:none}
.back-link{position:absolute;top:12px;left:12px;background:var(--surface);border:1px solid var(--border);
  border-radius:20px;padding:8px 14px;font-size:12px;font-weight:600;color:var(--text);text-decoration:none}
.section{padding:12px 12px 0;max-width:1200px;margin:0 auto}
.section-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:2px;
  color:var(--text-muted);margin-bottom:10px;margin-top:20px;padding-bottom:6px;border-bottom:1px solid var(--border-soft)}
.tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:20px;
  border-radius:8px;border:1px solid var(--border-soft)}
table{width:100%;border-collapse:collapse;font-size:11px;white-space:nowrap}
th{background:var(--surface);color:var(--text-muted);padding:7px 5px;text-align:center;
   font-weight:600;text-transform:uppercase;letter-spacing:0.4px;border-bottom:1px solid var(--border)}
th.left{text-align:left;padding-left:8px}
td{padding:6px 5px;text-align:center;border-bottom:1px solid var(--surface-deep);color:var(--text)}
td.name{text-align:left;padding-left:8px;font-weight:600;color:var(--text-strong);white-space:nowrap;
  position:sticky;left:0;background:var(--surface-2);z-index:1}
tr:nth-child(even) td.name{background:var(--surface-3)}
tr:hover td{background:var(--row-hover)}
tr:hover td.name{background:var(--row-hover-name)}
.hi{color:var(--green);font-weight:700}
.med{color:var(--yellow)}
.lo{color:var(--text-muted)}
.bad{color:var(--red);font-weight:700}
.dim{color:var(--text-faintest)}
.th-group{background:var(--th-group-bg);color:var(--text-faint);font-size:9px;letter-spacing:1px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-bottom:20px}
.card{background:var(--surface);border-radius:10px;padding:12px;border:1px solid var(--border)}
.card.available{border-color:#4ade8044}.card.soon{border-color:#fbbf2444}.card.unavailable{border-color:#f8714444}
.card .player-name{font-size:14px;font-weight:700;color:var(--text-strong);margin-bottom:6px}
.card .badge-row{display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap}
.card .pc{font-size:11px;color:var(--text-muted)}
.card .avail-msg{font-size:10px;color:var(--text-dim);margin-top:3px}
.card .l3-stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin-top:8px}
.card .l3-stat{text-align:center;background:var(--surface-deep);border-radius:6px;padding:5px 2px}
.card .l3-val{font-size:15px;font-weight:700;color:var(--accent)}
.card .l3-lbl{font-size:9px;color:var(--text-dim);text-transform:uppercase}
.game-row{display:flex;align-items:center;gap:8px;padding:8px 10px;
  background:var(--surface);border-radius:8px;margin-bottom:6px;font-size:13px;flex-wrap:wrap;
  text-decoration:none;color:inherit}
.game-row:hover{background:var(--row-hover-name)}
.game-row .result{font-weight:800;font-size:14px;min-width:24px}
.game-row .result.W{color:var(--green)}.game-row .result.L{color:var(--red)}.game-row .result.T{color:var(--yellow)}
.game-row .score{color:var(--accent);font-weight:700}
.game-row .opp{color:var(--text-muted);flex:1;min-width:120px}
.game-row .round{font-size:10px;color:var(--text-dim);background:var(--surface-deep);padding:2px 6px;border-radius:4px}
.game-row .arrow{color:var(--text-faint);font-size:12px}
.footer{text-align:center;padding:20px;font-size:11px;color:var(--text-faintest)}
.no-games{text-align:center;padding:40px;color:var(--text-faint);font-size:14px}
.dnp{color:var(--text-faintest);font-style:italic;font-size:10px}
.inning{background:var(--surface);border:1px solid var(--border-soft);border-radius:8px;margin-bottom:8px;overflow:hidden}
.inning summary{padding:10px 14px;font-weight:700;font-size:12px;letter-spacing:0.5px;cursor:pointer;
  color:var(--text-strong);text-transform:uppercase;list-style:none;display:flex;justify-content:space-between;align-items:center}
.inning summary::-webkit-details-marker{display:none}
.inning summary::after{content:"+";font-size:16px;color:var(--text-dim);font-weight:400}
.inning[open] summary::after{content:"–"}
.inning summary:hover{background:var(--row-hover)}
.play{padding:8px 14px;border-top:1px solid var(--border-soft)}
.play-header{font-weight:700;color:var(--text-strong);font-size:12px;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.play-header .tag{font-weight:600;color:var(--text-dim);font-size:10px;text-transform:uppercase}
.play-pitches{font-size:11px;color:var(--text-dim);margin-top:3px}
.play-desc{font-size:12px;color:var(--text-muted);margin-top:3px;line-height:1.5}
@media(max-width:768px){.section{padding:10px 8px 0}.cards{grid-template-columns:1fr 1fr}table{font-size:10px}th,td{padding:5px 4px}.game-row{font-size:12px}}
@media(max-width:480px){.record{gap:12px 16px}.cards{grid-template-columns:1fr 1fr}.card{padding:10px}.card .player-name{font-size:13px}table{font-size:10px}.section-title{font-size:11px;letter-spacing:1px}.game-row .opp{min-width:80px;font-size:11px}}
</style>"""

SCRIPT_BLOCK = """<script>
(function(){
  var t = localStorage.getItem('lightning-theme');
  if(!t){ t = (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) ? 'light' : 'dark'; }
  document.documentElement.setAttribute('data-theme', t);
})();
function toggleTheme(){
  var html = document.documentElement;
  var next = html.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', next);
  localStorage.setItem('lightning-theme', next);
}
</script>"""

THEME_TOGGLE_BUTTON = """  <button id="theme-toggle" onclick="toggleTheme()" aria-label="Toggle light/dark mode" title="Toggle light/dark mode">
    <span class="moon">🌙</span><span class="sun">☀️</span>
  </button>"""

BACK_LINK = '<a class="back-link" href="../index.html">← Dashboard</a>'


def head(title):
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
{CSS_BLOCK}
{SCRIPT_BLOCK}"""
