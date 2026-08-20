# -*- coding: utf-8 -*-
"""Render the CUSTOMER-FACING UBO briefing page from ubo_registry_intelligence.json.

Customer-safe by construction: no vendor names, no pricing we pay, no aggregation
architecture, no internal file paths. Everything shown here is about the REGISTERS.

Run: python scripts/render_ubo_briefing.py  ->  docs/generated/ubo_briefing.html
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "curation", "ubo_registry_intelligence.json")
OUT = os.path.join(ROOT, "docs", "generated", "ubo_briefing.html")

REGIME = {
    "public": "Open to anyone",
    "public_via_s2s": "Open on written application",
    "public_local_credentials": "Public in law, national eID in practice",
    "legitimate_interest": "Legitimate interest must be shown",
    "obliged_entities_only": "Regulated institutions only",
    "authorities_only": "Authorities only",
    "suspended": "Suspended",
    "closed": "Closed",
    "none": "No register",
}
MACHINE = {"api": "API", "portal": "Portal", "manual": "By email", "none": "None"}
COST = {"free": "Free", "per_document": "Per extract", "per_query": "Per query",
        "contract": "Contract", "mixed": "Mixed", "unknown": "Not published", "n/a": "—"}

TIERS = [
    ("open_direct", "Open", "Reachable today without local credentials."),
    ("direct_credentials", "Conditional", "Reachable, but an application, a contract or a national eID stands in the way."),
    ("customer_credentials", "Delegated", "Only a locally licensed institution may look — the credentials must be the customer's."),
    ("closed", "Closed", "Suspended, withdrawn, or reserved to authorities."),
    ("none", "Non-existent", "No beneficial-ownership register exists yet."),
]

NAME = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "HR": "Croatia", "CY": "Cyprus",
    "CZ": "Czechia", "DK": "Denmark", "EE": "Estonia", "FI": "Finland", "FR": "France",
    "DE": "Germany", "GR": "Greece", "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
    "LV": "Latvia", "LT": "Lithuania", "LU": "Luxembourg", "MT": "Malta",
    "NL": "Netherlands", "PL": "Poland", "PT": "Portugal", "RO": "Romania",
    "SK": "Slovakia", "SI": "Slovenia", "ES": "Spain", "SE": "Sweden",
    "GB": "United Kingdom", "CH": "Switzerland", "NO": "Norway", "LI": "Liechtenstein",
}

# Customer-safe one-liners. Deliberately NOT the internal notes.
NOTE = {
    "DK": "Free machine access to the register is granted on written application — no national eID needed. Watch the Danish substitute entry, where management is recorded because no person crosses 25%.",
    "GB": "Free public API and bulk download. Historically self-declared and unverified; the ECCTA identity checks are closing that gap.",
    "LV": "Latvia decided explicitly to stay public after the 2022 court ruling. Free to read; no official bulk channel.",
    "PL": "Fully public and free, with no registration — but portal-only, so there is no official machine channel.",
    "AT": "Applications from abroad are granted in practice. The extract carries a completeness flag no other register provides.",
    "DE": "Cheap and open in principle to regulated institutions. The queue is the constraint: waits of months to over a year are documented.",
    "EE": "Was the most open register in Europe. As measured this month the beneficial-owner query now demands an Estonian eID, and open-data publication is being withdrawn.",
    "FI": "Contractual access, granted to foreign institutions with justification. Covers private limited companies only — no listed companies, associations or foundations.",
    "FR": "The only large member state with a genuine API for beneficial ownership. Full access is entitlement-based and expects a French company identifier.",
    "LU": "Case-by-case and manual since 2022, at a small fee per request. Still not fully operational.",
    "MT": "One of the few registers that answers by email to a foreign applicant, with a low-cost subscription channel alongside.",
    "SE": "A clear process with an email route for foreigners. Sweden records the extent of control in bands, not a percentage — several owners can each show the maximum.",
    "SI": "Free, manual, and reportedly broad in what it accepts as an anti-money-laundering justification.",
    "BE": "Reopened under legitimate interest, but oriented to institutions with a Belgian presence. No machine channel.",
    "BG": "Beneficial-ownership data sits inside the commercial register; the detail is behind a Bulgarian qualified signature.",
    "HR": "Access runs through the national identity system, which a foreign company cannot obtain.",
    "IE": "Regulated Irish institutions have a working route. Applications on other grounds have been refused outright.",
    "LT": "The cheapest per-query price in Europe and bulk-capable — behind a Lithuanian eID.",
    "NL": "Reopened on 1 April 2026: a digitally certified extract, orderable by API, for recognised institutions. A structured JSON channel is planned for 2027.",
    "NO": "Built API-first with no public web interface at all. The data is machine-shaped; the entitlement is the wall.",
    "PT": "A legitimate-interest framework was decreed in late 2025 but is not yet deployed. Access needs the Portuguese citizen card.",
    "RO": "Public in principle, moving to legitimate interest, with a local electronic signature and explicit limits on redistribution.",
    "CY": "Public access ceased in January 2023. The register has run on and off since.",
    "CZ": "Had a working partial public channel and closed it in December 2025; access reverted to a court application.",
    "ES": "Nominally open to legitimate interest. In field testing the channel proved effectively non-functional, with waits of about six months.",
    "GR": "Public access suspended since December 2022.",
    "HU": "The criterion is circular: an applicant must already show a family, legal or ownership tie to the company whose owners they want to see.",
    "IT": "Built, then frozen by the courts pending a ruling from the Court of Justice. The framework is being restarted.",
    "LI": "Authorities and the financial intelligence unit only. Extracts carry no public reliance — the data is not verified by the authority.",
    "SK": "Public access to beneficial-ownership data was discontinued in July 2025. A separate register still discloses verified owners, but only for companies contracting with the public sector.",
    "CH": "Switzerland has no beneficial-ownership register at all today. The law adopted in September 2025 creates one, expected in autumn 2026 and restricted to domestic authorities and Swiss financial intermediaries.",
}

CLOCK = [
    ("22 Nov 2022", "The Court of Justice strikes down public access",
     "Joined Cases C-37/20 and C-601/20. Every closure on this page traces back to this ruling."),
    ("10 Jul 2025", "First deadline missed",
     "Infringement proceedings opened against 11 member states for missing the notification deadline."),
    ("10 Jul 2026", "Register-access rules fall due",
     "AMLD6 Articles 11-15: regulated institutions and legitimate-interest applicants regain a right of access."),
    ("10 Nov 2026", "The first date that makes automation realistic",
     "Registers must answer a legitimate-interest request within 12 working days, and approved applicants receive three-year certificates."),
    ("10 Jul 2027", "The AML Regulation applies in full",
     "Directly applicable in all 27 member states — but access portals, authentication and processing stay national."),
]

CSS = """
:root{
  --ground:#F2F3F5; --panel:#FFFFFF; --sunk:#E7E9ED;
  --ink:#16191F; --ink-2:#4A5160; --ink-3:#767E8E;
  --rule:#D3D7DE; --rule-soft:#E4E7EC;
  --accent:#2F4E7E;
  --open:#1F6B4F; --cond:#8A6510; --deleg:#8C4A2F; --closed:#8E3230; --nil:#6B7280;
  --open-bg:#E4F0EA; --cond-bg:#F5EBD8; --deleg-bg:#F5E7E0; --closed-bg:#F6E3E2; --nil-bg:#E9EBEF;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0F1218; --panel:#171B23; --sunk:#1F242E;
    --ink:#E9EBF0; --ink-2:#A8B0BF; --ink-3:#78808F;
    --rule:#2C333F; --rule-soft:#242A34;
    --accent:#8FB0E0;
    --open:#6FC79C; --cond:#DDAE52; --deleg:#DE9270; --closed:#E27B77; --nil:#98A0AE;
    --open-bg:#16281F; --cond-bg:#2B2416; --deleg-bg:#2C1E18; --closed-bg:#2C1A19; --nil-bg:#20242C;
  }
}
:root[data-theme="dark"]{
  --ground:#0F1218; --panel:#171B23; --sunk:#1F242E;
  --ink:#E9EBF0; --ink-2:#A8B0BF; --ink-3:#78808F;
  --rule:#2C333F; --rule-soft:#242A34;
  --accent:#8FB0E0;
  --open:#6FC79C; --cond:#DDAE52; --deleg:#DE9270; --closed:#E27B77; --nil:#98A0AE;
  --open-bg:#16281F; --cond-bg:#2B2416; --deleg-bg:#2C1E18; --closed-bg:#2C1A19; --nil-bg:#20242C;
}

*{box-sizing:border-box;}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
  font-size:16px; line-height:1.62; -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1080px; margin:0 auto; padding:0 24px 96px;}
.spine{max-width:66ch;}

h1,h2,h3{font-family:Newsreader,Georgia,"Times New Roman",serif; text-wrap:balance; margin:0;}
h1{font-size:clamp(2.3rem,5.4vw,3.7rem); line-height:1.06; font-weight:500; letter-spacing:-.015em;}
h2{font-size:clamp(1.5rem,2.6vw,2rem); line-height:1.15; font-weight:500;}
h3{font-size:1.12rem; font-weight:600; line-height:1.3;}
p{margin:0;}
a{color:var(--accent);}

.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.7rem; font-weight:500;
  letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3);
}

header.masthead{border-bottom:2px solid var(--ink); padding:56px 0 26px; display:flex; flex-direction:column; gap:20px;}
.standfirst{font-size:1.2rem; line-height:1.5; color:var(--ink-2); max-width:60ch;}
.meta{display:flex; flex-wrap:wrap; gap:8px 28px; padding-top:6px;}
.meta div{font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.74rem; color:var(--ink-3); letter-spacing:.03em;}
.meta b{color:var(--ink-2); font-weight:500;}

section{padding-top:60px; display:flex; flex-direction:column; gap:24px;}
.sec-head{display:flex; flex-direction:column; gap:10px;}

.verdict{
  background:var(--panel); border:1px solid var(--rule); border-left:none; border-right:none;
  padding:30px 0; display:flex; flex-direction:column; gap:14px;
}
.verdict .big{font-family:Newsreader,Georgia,serif; font-size:clamp(1.35rem,3vw,1.9rem); line-height:1.28; font-weight:500; max-width:34ch;}

.trio{display:grid; grid-template-columns:repeat(auto-fit,minmax(232px,1fr)); gap:1px; background:var(--rule-soft); border:1px solid var(--rule-soft);}
.trio > div{background:var(--panel); padding:22px; display:flex; flex-direction:column; gap:9px;}
.trio h3{font-family:"IBM Plex Sans",system-ui,sans-serif; font-size:.94rem; letter-spacing:.005em;}
.trio p{font-size:.9rem; color:var(--ink-2); line-height:1.55;}
.verdict-tag{
  font-family:"IBM Plex Mono",monospace; font-size:.66rem; letter-spacing:.12em; text-transform:uppercase;
  color:var(--closed); align-self:flex-start;
}

.tiles{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px;}
.tile{background:var(--panel); border:1px solid var(--rule-soft); padding:16px 18px 18px; display:flex; flex-direction:column; gap:4px;}
.tile .n{font-family:"IBM Plex Mono",monospace; font-size:2.5rem; line-height:1; font-weight:500; font-variant-numeric:tabular-nums;}
.tile .l{font-size:.83rem; font-weight:600; letter-spacing:.01em;}
.tile .d{font-size:.76rem; color:var(--ink-3); line-height:1.45;}
.t-open .n{color:var(--open);} .t-cond .n{color:var(--cond);}
.t-deleg .n{color:var(--deleg);} .t-closed .n{color:var(--closed);} .t-none .n{color:var(--nil);}

.band{display:flex; flex-direction:column; gap:0;}
.band-head{display:flex; align-items:baseline; gap:14px; flex-wrap:wrap; padding:0 0 10px; border-bottom:2px solid currentColor;}
.band-head .lbl{font-family:Newsreader,Georgia,serif; font-size:1.45rem; font-weight:500;}
.band-head .cnt{font-family:"IBM Plex Mono",monospace; font-size:.78rem; letter-spacing:.08em;}
.band-head .say{font-size:.88rem; color:var(--ink-2); flex:1 1 260px; min-width:0;}
.b-open{color:var(--open);} .b-cond{color:var(--cond);}
.b-deleg{color:var(--deleg);} .b-closed{color:var(--closed);} .b-none{color:var(--nil);}
.band-head .say, .band-head .cnt{color:var(--ink-2);}

.scroll{overflow-x:auto;}
table{width:100%; border-collapse:collapse; font-size:.87rem; min-width:720px;}
th{
  font-family:"IBM Plex Mono",monospace; font-size:.66rem; font-weight:500; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink-3); text-align:left; padding:12px 14px 10px; vertical-align:bottom;
  border-bottom:1px solid var(--rule);
}
td{padding:14px; border-bottom:1px solid var(--rule-soft); vertical-align:top; color:var(--ink-2);}
tr td:first-child{width:1%; white-space:nowrap;}
.jur{display:flex; align-items:baseline; gap:9px;}
.code{font-family:"IBM Plex Mono",monospace; font-size:1rem; font-weight:600; color:var(--ink); letter-spacing:.02em;}
.cty{font-size:.82rem; color:var(--ink-3);}
.reg{color:var(--ink); font-weight:500;}
td .who{display:block; margin-top:3px; font-size:.82rem; color:var(--ink-3);}
.chip{
  display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:.66rem; letter-spacing:.07em;
  text-transform:uppercase; padding:3px 8px; white-space:nowrap;
}
.c-api{background:var(--open-bg); color:var(--open);}
.c-portal,.c-email{background:var(--sunk); color:var(--ink-2);}
.c-none{background:var(--nil-bg); color:var(--nil);}
.note{font-size:.85rem; line-height:1.55;}

.clock{display:flex; flex-direction:column; gap:0; border-top:1px solid var(--rule);}
.beat{display:grid; grid-template-columns:132px 1fr; gap:20px; padding:18px 0; border-bottom:1px solid var(--rule-soft);}
.beat .d{font-family:"IBM Plex Mono",monospace; font-size:.78rem; color:var(--accent); letter-spacing:.02em; padding-top:3px;}
.beat h3{margin-bottom:4px;}
.beat p{font-size:.88rem; color:var(--ink-2);}
.past .d{color:var(--ink-3);}

.method{background:var(--sunk); padding:26px; display:flex; flex-direction:column; gap:12px;}
.method p{font-size:.87rem; color:var(--ink-2);}
footer{padding-top:56px; color:var(--ink-3); font-size:.8rem; border-top:1px solid var(--rule); margin-top:60px;}

@media (max-width:640px){
  .beat{grid-template-columns:1fr; gap:6px;}
  header.masthead{padding-top:36px;}
}
@media (prefers-reduced-motion:no-preference){
  a{transition:color .15s ease;}
}
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    rows = {r["jurisdiction"]: r for r in d["rows"]}
    order = {t: [] for t, _, _ in TIERS}
    for r in d["rows"]:
        order[r["verdict"]["tier"]].append(r)

    H = ['<title>Who Can Actually Read Europe’s UBO Registers</title>',
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&'
         'family=IBM+Plex+Sans:wght@400;500;600&'
         'family=IBM+Plex+Mono:wght@400;500;600&display=swap">',
         '<style>%s</style>' % CSS,
         '<div class="wrap">',
         '<header class="masthead">',
         '<div class="eyebrow">Market briefing · Beneficial ownership</div>',
         '<h1>Who can actually read Europe’s UBO registers</h1>',
         '<p class="standfirst">Every EU member state was required to keep a register of beneficial owners. '
         'Since the Court of Justice struck down public access in 2022, most of them have become unreadable '
         '— and no two are unreadable in the same way. This is what is left, jurisdiction by jurisdiction.</p>',
         '<div class="meta"><div><b>Scope</b> %s</div><div><b>Assessed</b> %s</div>'
         '<div><b>Basis</b> Registry publications, regulator sources, independent field testing</div></div>'
         % (esc(d["scope"]), esc(d["generated"])),
         '</header>']

    # Q1
    H += ['<section><div class="sec-head"><div class="eyebrow">The first question</div>',
          '<h2>Is there one place to get all of it?</h2></div>',
          '<div class="verdict"><p class="big">No. Three kinds of aggregation exist, and each one fails a '
          'different part of the requirement.</p></div>',
          '<div class="trio">',
          '<div><h3>The official interconnection</h3><p>The EU built BORIS to link the national registers through '
          'the e-Justice Portal. It still routes you through your own national register first, so a gated home '
          'register gates the interconnection too. Roughly 17 of 30 EU and EEA states have completed the '
          'technical connection; results come back as one static PDF at a time.</p>'
          '<div class="verdict-tag">Legally right, practically closed</div></div>',
          '<div><h3>Computed ownership graphs</h3><p>The large commercial databases infer ownership by walking '
          'shareholding chains across company registers — hundreds of millions of ownership links, worldwide '
          'coverage. But it is a calculation, not a filing. It can tell you who probably controls a company; it '
          'cannot produce the register entry, and it regularly disagrees with what the company itself declared.</p>'
          '<div class="verdict-tag">Broad, but not evidence</div></div>',
          '<div><h3>Live retrieval from the register</h3><p>Specialists fetch the real filing on request and '
          'time-stamp it. This is the right shape of answer — but their beneficial-ownership coverage collapses '
          'to the handful of registers that are actually reachable, because they meet exactly the same national '
          'walls. Headline claims of 200-plus jurisdictions describe company registers, not UBO registers.</p>'
          '<div class="verdict-tag">Right shape, thin coverage</div></div>',
          '</div>',
          '<p class="spine note">Which leaves the second question: what does it take to reach each register '
          'directly? That answer is different in all 31.</p>',
          '</section>']

    # tiles
    H += ['<section><div class="sec-head"><div class="eyebrow">The second question</div>',
          '<h2>What it takes, country by country</h2>',
          '<p class="spine standfirst" style="font-size:1rem">Four states of access. The dividing line that '
          'matters is not open versus closed — it is whether the credentials can be ours, or must be the '
          'regulated institution’s own.</p></div>',
          '<div class="tiles">']
    cls = {"open_direct": "t-open", "direct_credentials": "t-cond", "customer_credentials": "t-deleg",
           "closed": "t-closed", "none": "t-none"}
    for tier, label, blurb in TIERS:
        H.append('<div class="tile %s"><div class="n">%d</div><div class="l">%s</div><div class="d">%s</div></div>'
                 % (cls[tier], len(order[tier]), label, esc(blurb)))
    H.append('</div>')

    bcls = {"open_direct": "b-open", "direct_credentials": "b-cond", "customer_credentials": "b-deleg",
            "closed": "b-closed", "none": "b-none"}
    for tier, label, blurb in TIERS:
        rs = sorted(order[tier], key=lambda r: r["jurisdiction"])
        if not rs:
            continue
        H += ['<div class="band">',
              '<div class="band-head %s"><span class="lbl">%s</span><span class="cnt">%d of 31</span>'
              '<span class="say">%s</span></div>' % (bcls[tier], label, len(rs), esc(blurb)),
              '<div class="scroll"><table><thead><tr>'
              '<th>Jurisdiction</th><th>Register &amp; who may read it</th><th>Access</th><th>Cost</th>'
              '<th>What this means</th></tr></thead><tbody>']
        for r in rs:
            j = r["jurisdiction"]
            m = r["machineAccess"]
            chip = {"api": "c-api", "portal": "c-portal", "manual": "c-email", "none": "c-none"}[m]
            H.append(
                '<tr><td><span class="jur"><span class="code">%s</span><span class="cty">%s</span></span></td>'
                '<td><span class="reg">%s</span><span class="who">%s</span></td>'
                '<td><span class="chip %s">%s</span></td><td>%s</td><td class="note">%s</td></tr>'
                % (j, esc(NAME[j]), esc(r["registerName"]), esc(REGIME[r["accessRegime"]]),
                   chip, MACHINE[m], COST.get(r["cost"]["model"], r["cost"]["model"]), esc(NOTE[j])))
        H.append('</tbody></table></div></div>')
    H.append('</section>')

    # clock
    H += ['<section><div class="sec-head"><div class="eyebrow">What changes, and when</div>',
          '<h2>The reopening has a timetable</h2>',
          '<p class="spine standfirst" style="font-size:1rem">The closures were a court ruling; the reopening '
          'is a directive. These are the dates that decide whether any of this becomes automatable.</p></div>',
          '<div class="clock">']
    for i, (date, head, body) in enumerate(CLOCK):
        past = " past" if i < 2 else ""
        H.append('<div class="beat%s"><div class="d">%s</div><div><h3>%s</h3><p>%s</p></div></div>'
                 % (past, esc(date), esc(head), esc(body)))
    H += ['</div>',
          '<p class="spine note">One caution on all of it: the first deadline was already missed by eleven '
          'member states. Plans that assume the 2026 dates hold should carry a fallback.</p>',
          '</section>']

    # method
    H += ['<section><div class="sec-head"><div class="eyebrow">How this was assessed</div>'
          '<h2>Method, and where it is thin</h2></div>',
          '<div class="method spine">',
          '<p>Each jurisdiction was assessed on six things: whether a register exists, who is permitted to read '
          'it after the 2022 ruling, what credentials that permission actually requires, whether access is '
          'machine-readable, whether the output is a document or data fields, and what it costs.</p>',
          '<p>Sources are the registry operators’ own publications and regulator statements, supported by '
          'independent field testing of fourteen member states in September 2025 and by our own measurements '
          '— including the Estonian result on this page, which we verified directly and which contradicts '
          'every published comparison we could find.</p>',
          '<p>This is a first pass. Rows describing registers we have not yet applied to should be read as '
          'well-sourced but untested, and several member states are mid-transition: Italy is awaiting a court '
          'ruling, Switzerland is standing a register up, the Netherlands is adding a structured data channel, '
          'and Estonia is closing one.</p>',
          '</div></section>',
          '<footer>Prepared %s · EU-27 plus the United Kingdom, Switzerland, Norway and Liechtenstein · '
          'Register access regimes change without notice; verify before relying on any single row.</footer>'
          % esc(d["generated"]),
          '</div>']

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(H) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
