"""Render curation/document_kinds_evidence.json into a self-contained HTML review page.

One file, no dependencies, no server: open docs/document_kinds_review.html in any browser
(double-click). The evidence JSON is embedded, so it works offline and can be emailed.

Filter by jurisdiction / kind / status; each row expands to show the cited evidence
(statute, verbatim quote, source link) and caveats. This is the reviewer's view of the
same data the API would serve — nothing here that isn't in the JSON.

Run:
    python scripts/render_html_review.py
"""
import os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "curation", "document_kinds_evidence.json")
OUT = os.path.join(ROOT, "docs", "document_kinds_review.html")

STATUS_LABEL = {
    "proved_by_base_document": ("Base document", "#137333", "#e6f4ea"),
    "proved_by_additional_document": ("Additional document", "#b06000", "#fef7e0"),
    "not_provable_from_registry": ("Not provable", "#a50e0e", "#fce8e6"),
    "not_researched": ("Not researched", "#5f6368", "#f1f3f4"),
}
KIND_LABEL = {
    "REGISTERAUSZUG": "Registerauszug",
    "GESELLSCHAFTERLISTE": "Gesellschafterliste",
    "GESELLSCHAFTSVERTRAG": "Gesellschaftsvertrag",
}


def main():
    rows = json.load(open(SRC, encoding="utf-8"))
    # Merge the routing decision (the ACTIONABLE answer) onto each evidence row so the page
    # is answer-first: the decision leads, the citations sit underneath as the "why".
    routing = os.path.join(ROOT, "curation", "document_kinds_routing.json")
    if os.path.exists(routing):
        rt = {(x["jurisdiction"], x["legalForm"], x["kind"]): x
              for x in json.load(open(routing, encoding="utf-8"))["routes"]}
        for r in rows:
            d = rt.get((r["jurisdiction"], r["legalForm"], r["kind"]))
            if d:
                r["_answer"] = {k: d[k] for k in ("availability", "action", "completeness",
                                                  "vendor", "fallback", "flags", "order")}
    # Embed as raw JSON in a <script type="application/json"> block. Do NOT HTML-escape:
    # browsers don't decode entities inside <script>, so &quot; would break JSON.parse.
    # Only neutralize < and > (present in values like ">=5%", "<dd/mm/yyyy>") as \u
    # escapes — valid inside JSON strings and prevents any "</script>" breakout.
    data = (json.dumps(rows, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e"))
    jurisdictions = sorted({r["jurisdiction"] for r in rows})
    n_juris = len(jurisdictions)
    ev = [e for r in rows for e in r.get("evidence", [])]
    quoted = len([e for e in ev if e.get("quote")])

    page = TEMPLATE.replace("__DATA__", data)
    page = page.replace("__NROWS__", str(len(rows)))
    page = page.replace("__NJURIS__", str(n_juris))
    page = page.replace("__NEV__", str(len(ev)))
    page = page.replace("__PCTQUOTE__", str(round(100 * quoted / len(ev)) if ev else 0))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print("Wrote %s (%d rows, %d jurisdictions)" % (os.path.relpath(OUT, ROOT), len(rows), n_juris))


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Document kinds — what each registry evidences</title>
<style>
 :root { --bg:#fff; --fg:#202124; --muted:#5f6368; --line:#e0e0e0; --accent:#1a73e8; }
 * { box-sizing: border-box; }
 body { margin:0; font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
        color:var(--fg); background:#f8f9fa; }
 header { background:var(--bg); border-bottom:1px solid var(--line); padding:20px 24px; }
 h1 { margin:0 0 4px; font-size:20px; }
 .sub { color:var(--muted); font-size:13px; }
 .wrap { max-width:1100px; margin:0 auto; padding:0 24px 60px; }
 .controls { position:sticky; top:0; background:#f8f9fa; padding:16px 0; z-index:5;
             display:flex; gap:10px; flex-wrap:wrap; align-items:center;
             border-bottom:1px solid var(--line); }
 select, input { font:inherit; padding:7px 10px; border:1px solid var(--line);
                 border-radius:8px; background:#fff; }
 input { flex:1; min-width:180px; }
 .count { color:var(--muted); font-size:13px; margin-left:auto; }
 details.j { background:#fff; border:1px solid var(--line); border-radius:12px;
             margin:14px 0; overflow:hidden; }
 details.j > summary { padding:14px 18px; font-weight:600; font-size:16px; cursor:pointer;
                       list-style:none; display:flex; align-items:center; gap:10px; }
 details.j > summary::-webkit-details-marker { display:none; }
 .jflag { color:var(--muted); font-weight:400; font-size:13px; }
 .row { border-top:1px solid var(--line); padding:14px 18px; }
 .rhead { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
 .kind { font-weight:600; }
 .form { color:var(--muted); font-size:13px; }
 .badge { font-size:12px; font-weight:600; padding:2px 9px; border-radius:20px; }
 .answer { margin:6px 0 2px; display:flex; flex-wrap:wrap; align-items:center; gap:8px; }
 .abits { font-size:12px; color:var(--muted); }
 .doc { font-size:13px; margin-top:5px; }
 .doc b { font-weight:600; }
 .summary { margin:7px 0 0; font-size:14px; }
 .conf { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.03em; }
 details.ev > summary { cursor:pointer; color:var(--accent); font-size:13px; margin-top:8px;
                        list-style:none; }
 details.ev > summary::-webkit-details-marker { display:none; }
 details.ev > summary::before { content:"▸ "; }
 details.ev[open] > summary::before { content:"▾ "; }
 blockquote { margin:8px 0; padding:8px 12px; border-left:3px solid var(--line);
              background:#fafafa; font-size:13px; }
 blockquote .basis { font-weight:600; display:block; margin-bottom:3px; }
 blockquote .q { font-style:italic; color:#3c4043; }
 blockquote .n { color:var(--muted); font-size:12px; display:block; margin-top:3px; }
 a { color:var(--accent); }
 .caveats { margin:8px 0 0; padding:0 0 0 18px; font-size:12.5px; color:#5f6368; }
 .caveats li { margin:2px 0; }
 .flagword { color:#a50e0e; font-weight:600; }
 @media (prefers-color-scheme: dark) {
  :root { --bg:#202124; --fg:#e8eaed; --muted:#9aa0a6; --line:#3c4043; --accent:#8ab4f8; }
  body { background:#171717; } .controls { background:#171717; }
  select,input,blockquote { background:#2a2b2e; } blockquote { background:#2a2b2e; }
  details.j { background:#202124; }
 }
</style>
</head>
<body>
<header>
 <div class="wrap" style="padding-bottom:0">
  <h1>Document kinds — what each registry actually evidences</h1>
  <div class="sub">Per jurisdiction &amp; legal form: the <b>actionable answer</b> (what to do to
   get each document kind) with the cited evidence beneath it. <b>A document is the proof</b> —
   parsed data is not credited. Vendor-neutral. Germany out of scope. __NROWS__ rows ·
   __NJURIS__ jurisdictions · __NEV__ cited sources (__PCTQUOTE__% verbatim-quoted).</div>
 </div>
</header>
<div class="wrap">
 <div class="controls">
  <select id="fj"><option value="">All jurisdictions</option></select>
  <select id="fk">
   <option value="">All kinds</option>
   <option value="REGISTERAUSZUG">Registerauszug</option>
   <option value="GESELLSCHAFTERLISTE">Gesellschafterliste</option>
   <option value="GESELLSCHAFTSVERTRAG">Gesellschaftsvertrag</option>
  </select>
  <select id="fs">
   <option value="">All answers</option>
   <option value="use_delivered">Use delivered (base)</option>
   <option value="order">Order (additional)</option>
   <option value="manual">Manual / fallback</option>
   <option value="unavailable">Unavailable</option>
  </select>
  <input id="q" placeholder="Search text, statute, document…">
  <span class="count" id="count"></span>
 </div>
 <div id="list"></div>
</div>
<script type="application/json" id="data">__DATA__</script>
<script>
const ROWS = JSON.parse(document.getElementById('data').textContent);
const STATUS = {
 proved_by_base_document:['Base document','#137333','#e6f4ea'],
 proved_by_additional_document:['Additional document','#b06000','#fef7e0'],
 not_provable_from_registry:['Not provable','#a50e0e','#fce8e6'],
 not_researched:['Not researched','#5f6368','#f1f3f4']};
const KIND = {REGISTERAUSZUG:'Registerauszug',GESELLSCHAFTERLISTE:'Gesellschafterliste',
 GESELLSCHAFTSVERTRAG:'Gesellschaftsvertrag'};
const esc = s => (s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const flag = s => esc(s).replace(/(UNVERIFIED|INFERENCE|CONFLICT|CRITICAL|CRUX|KEY POINT|EXCEPTION|THRESHOLD|NOMINEE|STALENESS)/g,'<span class="flagword">$1</span>');
for (const j of [...new Set(ROWS.map(r=>r.jurisdiction))].sort())
 document.getElementById('fj').insertAdjacentHTML('beforeend',`<option>${j}</option>`);
function evHTML(e){
 let q = e.quote?`<span class="q">„${esc(e.quote)}"</span>`:'';
 let n = e.note?`<span class="n">${esc(e.note)}</span>`:'';
 let u = e.url?`<span class="n"><a href="${esc(e.url)}" target="_blank" rel="noopener">${esc(e.url)}</a> · ${esc(e.retrieved||'')}</span>`:'';
 return `<blockquote><span class="basis">${esc(e.basis||'')}</span>${q}${n}${u}</blockquote>`;
}
const ACTION = {
 use_delivered:['✔ Use delivered document','#137333','#e6f4ea'],
 use_delivered_with_warning:['✔ Use delivered — check completeness','#b06000','#fef7e0'],
 order:['＋ Order (additional)','#1a56c4','#e8f0fe'],
 order_with_warning:['＋ Order — check completeness','#b06000','#fef7e0'],
 manual:['✋ No registry doc — use fallback','#a50e0e','#fce8e6'],
 unavailable:['✖ Not available here','#5f6368','#f1f3f4']};
const answerHTML = a => {
 if(!a) return '';
 const [lab,fg,bg] = ACTION[a.action]||['?','#000','#eee'];
 const bits = [];
 if(a.completeness && a.completeness!=='full') bits.push(`completeness: <b>${esc(a.completeness)}</b>`);
 (a.flags||[]).filter(f=>f==='nominee').forEach(()=>bits.push('<b class="flagword">registered ≠ beneficial (nominee)</b>'));
 if(a.action==='manual'&&a.fallback) bits.push(`fallback: <b>${esc(a.fallback)}</b>`);
 if(a.vendor) bits.push(`vendor: ${esc(a.vendor)}`);
 if(a.order&&a.order.model) bits.push(`ordering: ${esc(a.order.model)}`);
 return `<div class="answer"><span class="badge" style="color:${fg};background:${bg};font-size:13px">${lab}</span>${bits.length?' <span class="abits">'+bits.join(' · ')+'</span>':''}</div>`;
};
function rowHTML(r){
 const [lab,fg,bg] = STATUS[r.status]||['?','#000','#eee'];
 const doc = (r.documentLocal||r.documentLabel)
   ? `<div class="doc"><b>Document:</b> ${esc(r.documentLocal||'')}${r.documentLabel&&r.documentLabel!==r.documentLocal?' — '+esc(r.documentLabel):''}</div>`:'';
 const cav = (r.caveats&&r.caveats.length)
   ? `<ul class="caveats">${r.caveats.map(c=>`<li>${flag(c)}</li>`).join('')}</ul>`:'';
 const best = r.bestAvailable?`<div class="doc"><b>Best available:</b> ${esc(r.bestAvailable)}</div>`:'';
 const ev = (r.evidence&&r.evidence.length)
   ? `<details class="ev"><summary>${r.evidence.length} cited source${r.evidence.length>1?'s':''}${cav?' + caveats':''}</summary>${r.evidence.map(evHTML).join('')}${cav}</details>`
   : cav;
 return `<div class="row">
   <div class="rhead">
     <span class="kind">${KIND[r.kind]||r.kind}</span>
     <span class="form">${esc(r.legalForm)}</span>
     <span class="conf">${esc(r.confidence||'')}</span>
   </div>${answerHTML(r._answer)}${doc}${best}<div class="summary">${esc(r.summary||'')}</div>${ev}</div>`;
}
function render(){
 const fj=fjEl.value, fk=fkEl.value, fs=fsEl.value, q=qEl.value.toLowerCase();
 const rows = ROWS.filter(r=>(!fj||r.jurisdiction===fj)&&(!fk||r.kind===fk)
   &&(!fs||(r._answer&&r._answer.action&&r._answer.action.startsWith(fs)))
   &&(!q||JSON.stringify(r).toLowerCase().includes(q)));
 const byJ={};
 for(const r of rows)(byJ[r.jurisdiction]=byJ[r.jurisdiction]||[]).push(r);
 const order=['REGISTERAUSZUG','GESELLSCHAFTERLISTE','GESELLSCHAFTSVERTRAG'];
 let out='';
 for(const j of Object.keys(byJ).sort()){
  const rs=byJ[j].sort((a,b)=>order.indexOf(a.kind)-order.indexOf(b.kind)||a.legalForm.localeCompare(b.legalForm));
  const open = fj||q ? 'open':'';
  out+=`<details class="j" ${open}><summary>${j} <span class="jflag">${rs.length} row${rs.length>1?'s':''}</span></summary>${rs.map(rowHTML).join('')}</details>`;
 }
 listEl.innerHTML = out || '<p style="color:#5f6368">No rows match.</p>';
 countEl.textContent = rows.length+' / '+ROWS.length+' rows';
}
const fjEl=document.getElementById('fj'),fkEl=document.getElementById('fk'),
 fsEl=document.getElementById('fs'),qEl=document.getElementById('q'),
 listEl=document.getElementById('list'),countEl=document.getElementById('count');
[fjEl,fkEl,fsEl].forEach(e=>e.onchange=render); qEl.oninput=render;
render();
</script>
</body>
</html>"""


if __name__ == "__main__":
    main()
