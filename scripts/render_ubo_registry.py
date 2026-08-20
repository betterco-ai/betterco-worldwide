# -*- coding: utf-8 -*-
"""Render ubo_registry_intelligence.json into the internal UBO market document.

Run: python scripts/render_ubo_registry.py  ->  docs/UBO_REGISTRY_INTELLIGENCE.md
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "curation", "ubo_registry_intelligence.json")
OUT = os.path.join(ROOT, "docs", "UBO_REGISTRY_INTELLIGENCE.md")

TIER = {
    "open_direct":          "\U0001F7E2 Open — reachable now",
    "direct_credentials":   "\U0001F7E1 Direct, credentials or contract needed",
    "customer_credentials": "\U0001F7E0 Only under a local obliged entity's credentials",
    "closed":               "\U0001F534 Closed, suspended or authorities-only",
    "none":                 "⚫ No register exists",
}
ORDER = ["open_direct", "direct_credentials", "customer_credentials", "closed", "none"]

MACHINE = {"api": "API", "portal": "portal only", "manual": "manual / email", "none": "none"}


def src_line(s):
    return "[%s](%s)" % (s["basis"], s["url"])


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    rows = d["rows"]
    by_tier = {t: [r["jurisdiction"] for r in rows if r["verdict"]["tier"] == t] for t in ORDER}

    L = ["# UBO registers — market analysis and direct-connectivity map (INTERNAL)", "",
         "**Scope:** %s · **Generated:** %s · **Pass:** %s" % (d["scope"], d["generated"], d["pass"]), "",
         "> %s" % d["note"], "",
         "Sibling of `REGISTRY_INTELLIGENCE.md`. That document answers *can we reach the COMPANY register "
         "directly*. This one asks the same question of the **beneficial-ownership register** — a different "
         "register, a different legal basis, and a far harsher access regime.", "",
         "---", "", "## 1. Is there an aggregator? (Q1)", "",
         "**%s**" % d["market"]["answer"], ""]

    for a in d["market"]["archetypes"]:
        L += ["### %s" % a["name"], "",
              "- **Who:** %s" % a["operator"],
              "- **What it is:** %s" % a["whatItIs"],
              "- **Why it fails us:** %s" % a["whyItFails"],
              "- **Sources:** %s" % "; ".join(src_line(s) for s in a["sources"]), ""]

    L += ["### The measurement we already own", "", d["market"]["inHouseEvidence"], "",
          "### Also relevant", "", d["market"]["closedAggregator"], "",
          "### The regulatory clock", ""]
    rc = d["market"]["regulatoryClock"]
    LABEL = {"cjeu": "CJEU", "amld6": "AMLD6", "art13": "AMLD6 Art. 13", "reality": "Reality check"}
    for k in ("cjeu", "amld6", "art13", "reality"):
        L.append("- **%s:** %s" % (LABEL[k], rc[k]))
    L += ["- **Sources:** %s" % "; ".join(src_line(s) for s in rc["sources"]), "",
          "---", "", "## 2. Direct connectivity by country (Q2)", "", "### Scorecard", "",
          "| Verdict | Jurisdictions |", "|---|---|"]
    for t in ORDER:
        if by_tier[t]:
            L.append("| %s | %s |" % (TIER[t], ", ".join(sorted(by_tier[t]))))

    L += ["", "### At a glance", "",
          "| | Register | Access regime | Foreign access | Machine access | Cost | Verdict | Conf. |",
          "|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (ORDER.index(x["verdict"]["tier"]), x["jurisdiction"])):
        L.append("| **%s** | %s | %s | %s | %s | %s | %s | %s |" % (
            r["jurisdiction"], r["registerName"], r["accessRegime"], r["foreignAccess"],
            MACHINE.get(r["machineAccess"], r["machineAccess"]), r["cost"]["model"],
            TIER[r["verdict"]["tier"]].split(" ", 1)[0], r["confidence"]))

    L += ["", "---", "", "## 3. What we do about it", "",
          "| # | Where | Action | Why it matters | Cost |", "|---|---|---|---|---|"]
    for a in d["actions"]:
        L.append("| %d | %s | %s | %s | %s |" % (a["prio"], a["who"], a["action"], a["why"], a["cost"]))

    L += ["", "---", "", "## 4. Per jurisdiction", ""]
    for r in sorted(rows, key=lambda x: (ORDER.index(x["verdict"]["tier"]), x["jurisdiction"])):
        L += ["### %s — %s" % (r["jurisdiction"], r["registerName"]), "",
              "**%s** — %s" % (TIER[r["verdict"]["tier"]], r["verdict"]["reason"]), "",
              "- **Body:** %s%s" % (r["registerBody"], "" if r["separateRegister"] else " · *held inside the company register, not separately*"),
              "- **Who may access:** %s" % r["whoCanAccess"],
              "- **Foreign access:** %s · **credentials:** %s" % (r["foreignAccess"], r["credentials"]),
              "- **Machine access:** %s · delivers: %s · document via API: **%s**" % (
                  MACHINE.get(r["machineAccess"], r["machineAccess"]),
                  ", ".join(r["delivers"]) or "nothing", "yes" if r["documentViaApi"] else "no"),
              "- **Cost (%s):** %s" % (r["cost"]["model"], r["cost"]["detail"]),
              "- **BORIS:** %s · **vendor today:** %s" % (r["boris"], r["vendorToday"]),
              "- **Notes:** %s" % r["notes"],
              "- **Confidence:** %s" % r["confidence"],
              "- **Sources:** %s" % "; ".join(src_line(s) for s in r["sources"]),
              "- **URL:** <%s>" % r["registerUrl"], ""]

    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", OUT, "-", len(rows), "rows")


if __name__ == "__main__":
    main()
