import json, html
esol = json.load(open("/home/claude/build/esol.json"))
docs = json.load(open("/home/claude/build/docs.json"))
def _li(x): return f'<li><a href="{x["path"][:-5]}.pdf" target="_blank" rel="noopener">{html.escape(x["title"])}</a> <a class="tag" href="{x["path"]}" download>Word ⬇</a></li>'
def dl(folder):
    d=[x for x in docs if x["folder"]==folder and not x.get("group")]
    g=[x for x in docs if x["folder"]==folder and x.get("group")]
    out=""
    if d: out+='<h4>Worksheets and plans</h4><p class="hint">Click a title to view it. Use the Word button to download and edit.</p><ul class="docs">'+"".join(_li(x) for x in d)+"</ul>"
    if g:
        import re as _re
        les={}
        for x in g:
            m=_re.match(r"Lesson (\d+): (.*) – (plan and answers|student handouts)",x["title"]); les.setdefault(int(m[1]),{"t":m[2]})[m[3]]=x
        rows=""
        for n in sorted(les):
            L=les[n]; parts=[]
            for key,lab in (("plan and answers","Plan"),("student handouts","Handouts")):
                if key in L: x=L[key]; parts.append(f'<a href="{x["path"][:-5]}.pdf" target="_blank" rel="noopener">{lab}</a> <a class="tag" href="{x["path"]}" download>Word ⬇</a>')
            rows+=f'<li><b>Lesson {n}:</b> {html.escape(L["t"])}<span class="links">{" ".join(parts)}</span></li>'
        out+=f'<details class="course"><summary>ESB exam prep course – {len(les)} two-hour lessons</summary><ol class="docs les">{rows}</ol></details>'
    return out

LOGO = open("/home/claude/build/logo.html").read()

LEVELS = [("e1","Entry 1"),("e2","Entry 2"),("e3","Entry 3"),("l1","Level 1"),("l2","Level 2")]
SKILLS = [("reading","Reading"),("writing","Writing"),("speaking-listening","Speaking & Listening")]
EXTRA = [("all-levels","All levels"),("games","Games")]

def items(folder):
    return [e for e in esol if e["folder"] == folder]

def li(e):
    note = f'<span class="note">{html.escape(e["note"])}</span>' if e["note"] else ""
    return f'<li><a href="{e["path"]}">{html.escape(e["title"])}</a>{note}</li>'

grid = []
for lk, ln in LEVELS:
    cells = []
    for sk, sn in SKILLS:
        its = items(f"{lk}/{sk}")
        n = len(its); nd = len([x for x in docs if x["folder"]==f"{lk}/{sk}" and not x.get("group")]); nl=len({x["path"].split("/")[-1][:9] for x in docs if x["folder"]==f"{lk}/{sk}" and x.get("group")})
        cells.append(f'<a class="cell{"" if n or nd or nl else " empty"}" href="#{lk}-{sk}"><b>{sn}</b><span>{" · ".join(p for p in [f"{n} online" if n else "", f"{nd} Word" if nd else "", f"{nl} lessons" if nl else ""] if p) or "–"}</span></a>')
    grid.append(f'<div class="lvl"><h3>{ln}</h3>{"".join(cells)}</div>')

sections = []
for lk, ln in LEVELS:
    for sk, sn in SKILLS:
        its = items(f"{lk}/{sk}")
        f0=f"{lk}/{sk}"
        body = (f'<ol>{"".join(li(e) for e in its)}</ol>' if its else '') + dl(f0)
        if not body: body = '<p class="empty-t">Nothing here yet.</p>'
        sections.append(f'<section id="{lk}-{sk}"><h2>{ln} – {sn}</h2>{body}</section>')
for f, n in EXTRA:
    sections.append(f'<section id="{f}"><h2>{n}</h2><ol>{"".join(li(e) for e in items(f))}</ol>{dl(f)}</section>')

page = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESOL Library</title>
<style>
:root{{--bg:#f6f7f4;--card:#fff;--ink:#1f2a24;--muted:#5c6b62;--line:#dde3dc;--accent:#1d6b54;--soft:#e1efe9}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141a17;--card:#1c2420;--ink:#e7ede9;--muted:#9fb0a6;--line:#2d3833;--accent:#5cc3a0;--soft:#1f3a30}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Verdana,Arial,sans-serif}}
.wrap{{max-width:1100px;margin:0 auto;padding:24px 16px 120px}}
h1{{font-size:1.8rem;margin:0 0 4px}}
.top{{display:flex;align-items:center;gap:14px;flex-direction:row-reverse;justify-content:space-between}}
.top .atin-logo{{position:static!important;inset:auto!important;margin:0!important;flex:none}}
.sub{{color:var(--muted);margin:0 0 24px}}
.grid{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}}
@media (max-width:1000px){{.grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
@media (max-width:640px){{.grid{{grid-template-columns:minmax(0,1fr)}}}}
.lvl{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:8px}}
.lvl h3{{margin:0;font-size:1.05rem}}
.cell{{display:flex;flex-direction:column;gap:2px;padding:8px 10px;border-radius:8px;background:var(--soft);color:var(--ink);text-decoration:none;font-size:.9rem}}
.cell span{{color:var(--muted);font-size:.8rem}}
.cell.empty{{background:transparent;border:1px dashed var(--line)}}
.cell:hover b{{text-decoration:underline}}
.extra{{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 0}}
.extra a{{padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);text-decoration:none}}
section{{margin-top:32px}}
h2{{font-size:1.25rem;border-bottom:2px solid var(--accent);padding-bottom:6px}}
ol{{padding-left:22px}} li{{margin:6px 0}}
li a{{color:var(--accent);font-weight:bold}}
.note{{display:block;color:var(--muted);font-size:.85rem}}
h4{{margin:18px 0 4px;font-size:1rem;color:var(--muted)}}
.docs{{padding-left:22px}} .docs a{{color:var(--accent)}}
.docs li a.tag{{font-size:.8rem;font-weight:normal;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:1px 6px;margin-left:6px;text-decoration:none;white-space:nowrap}}
.docs li a.tag:hover{{color:var(--accent);border-color:var(--accent)}}
.course{{margin:16px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px}}
.course summary{{cursor:pointer;font-weight:bold;color:var(--accent)}}
.les{{list-style:none;padding-left:0}} .les li{{padding:6px 0;border-top:1px solid var(--line)}}
.les .links{{display:block;margin-top:2px}} .les .links a:not(.tag){{margin-right:2px}} .les .links a.tag{{margin-right:18px}}
.hint{{color:var(--muted);font-size:.85rem;margin:0 0 4px}}
.empty-t{{color:var(--muted);font-style:italic}}
</style></head><body><div class="wrap">
<header class="top">{LOGO}<h1>ESOL Library</h1></header>
<p class="sub">Online activities, projector lessons, games and Word documents for ESOL classes, Entry 1 to Level 2.</p>
<div class="grid">{"".join(grid)}</div>
<div class="extra">{"".join(f'<a href="#{f}">{n}</a>' for f,n in EXTRA)}</div>
{"".join(sections)}
</div>
</body></html>"""
open("/home/claude/esol/index.html", "w").write(page)

readme = ["# ESOL Library", "", "Online ESOL activities, projector lessons and games, Entry 1 to Level 2. Made by Atin.", "",
          "Live site: https://atinwix.github.io/esol/", "", "Each level has three strands: Reading, Writing, Speaking & Listening.", ""]
for f in sorted({e["folder"] for e in esol}):
    readme.append(f"## {f}")
    for e in items(f):
        readme.append(f"- [{e['title']}]({e['path']})" + (f" – {e['note']}" if e["note"] else ""))
    d=[x for x in docs if x["folder"]==f]
    if d:
        d=sorted(d,key=lambda x:(bool(x.get("group")),x["path"]))
        readme.append(""); readme.append("Word documents:")
        for x in d: readme.append(f"- [{x['title']}]({x['path'][:-5]}.pdf) (PDF) · [Word]({x['path']})")
    readme.append("")
open("/home/claude/esol/README.md", "w").write("\n".join(readme))
print("ok")
