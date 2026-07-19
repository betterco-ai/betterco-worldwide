"""Render registry_intelligence.json into an internal build-vs-buy document.

Run: python scripts/render_registry.py  ->  docs/REGISTRY_INTELLIGENCE.md
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "curation", "registry_intelligence.json")
OUT = os.path.join(ROOT, "docs", "REGISTRY_INTELLIGENCE.md")

VERDICT = {
    "direct_strong": "🟢 Go direct (strong)",
    "direct_good": "🟢 Go direct (paid docs)",
    "direct_contract": "🟡 Direct, contract needed",
    "direct_data_only": "🟠 Direct for DATA only — vendor for documents",
    "vendor_only": "🔴 Vendor only (no usable API)",
}
ORDER = ["direct_strong", "direct_good", "direct_contract", "direct_data_only", "vendor_only"]


def main():
    rows = {r["jurisdiction"]: r for r in json.load(open(SRC, encoding="utf-8"))}
    L = ["# Registry intelligence — build vs. buy (INTERNAL)", "",
         "For each analysed jurisdiction: what the registry is, whether it has an open API "
         "(and whether that API serves **documents** or only data), and the cost — to decide "
         "where we can integrate **directly** instead of paying an aggregation vendor.",
         "", "> Verdict driver: the prize is a registry we can hit directly that also serves the "
         "**documents** (not just data), cheaply. Data-only or no-API → keep the vendor for filings.",
         "", "## Scorecard", "",
         "| Verdict | Jurisdictions |", "|---|---|"]
    by = {}
    for r in rows.values():
        by.setdefault(r["goDirect"]["verdict"], []).append(r["jurisdiction"])
    for v in ORDER:
        if by.get(v):
            L.append("| %s | %s |" % (VERDICT[v], ", ".join(sorted(by[v]))))
    L += ["", "## Per jurisdiction", ""]

    for j in sorted(rows):
        r = rows[j]
        gd = r["goDirect"]
        L.append("### %s — %s" % (j, r["registryName"]))
        L.append("")
        L.append("**%s** — %s" % (VERDICT[gd["verdict"]], gd["reason"]))
        L.append("")
        L.append("- **Body:** %s" % r.get("registryBody", "—"))
        L.append("- **Open API:** %s%s%s" % (
            r["openApi"],
            " · " + r["apiName"] if r.get("apiName") else "",
            " · docs: <%s>" % r["apiDocsUrl"] if r.get("apiDocsUrl") else ""))
        L.append("- **Delivers:** %s | documents via API: **%s**" % (
            ", ".join(r.get("apiDelivers") or []) or "—",
            "yes" if r.get("documentsViaApi") else "no"))
        L.append("- **Auth:** %s" % r.get("apiAuth", "—"))
        L.append("- **Cost (%s):** %s" % (r["cost"].get("model"), r["cost"].get("detail", "")))
        if r.get("notes"):
            L.append("- **Notes:** %s" % r["notes"])
        L.append("- **Confidence:** %s" % r.get("confidence", "—"))
        srcs = r.get("sources") or []
        if srcs:
            L.append("- **Sources:** " + "; ".join("[%s](%s)" % (s.get("basis", "src"), s.get("url"))
                                                    for s in srcs if s.get("url")))
        L.append("")

    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print("Wrote %s (%d jurisdictions)" % (os.path.relpath(OUT, ROOT), len(rows)))


if __name__ == "__main__":
    main()
