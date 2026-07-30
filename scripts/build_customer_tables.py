# -*- coding: utf-8 -*-
"""Erzeugt die Kundentabellen fuer Leistungsbeschreibung und Deck AUS DEN DATENDATEIEN.

Zweck: Keine handgetippten Zellwerte und keine handgezaehlten Summen mehr in
kundenseitigen Dokumenten. Jede Zahl in der Ausgabe ist abgeleitet, nicht gesetzt.

Hintergrund: Am 2026-07-30 stand im Kundendeck die Aussage, ein registerseitiger
Nachweis der Anteilsinhaber existiere in "genau drei der fuenfzehn Maerkte". Die
Evidenzdatei sagte acht. Der Fehler sass nicht in den Daten, sondern in der
handgeschriebenen Prosa darueber. Dieses Skript schliesst diese Fehlerklasse fuer
die Tabellen; fuer Fliesstext bleibt die Behauptungspruefung zustaendig.

Eingaben (read-only):
    jurisdiction_matrix.json                 Vendor-Katalog (mandatory / non-mandatory)
    curation/registry_intelligence.json      goDirect-Verdikt, Kosten, Lizenz
    curation/document_kinds_routing.json     abgeleitete Routen
Ausgabe:
    docs/generated/customer_tables.md        Fragmente + Herleitung + Selbstpruefung

Aufruf:  python scripts/build_customer_tables.py
"""
from __future__ import annotations
import io, json, os, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STP15 = ["FR", "IT", "GB", "US", "ES", "DK", "NL", "LU", "CH", "IL",
         "JP", "BE", "KW", "SG", "HK"]

# Unser eigener Anbindungsstand. Das ist KEINE Registereigenschaft, sondern
# Projektzustand -- deshalb hier explizit und benannt, nicht aus Daten abgeleitet.
DIRECT_PRODUCTIVE = {"DE", "FR", "GB"}
DIRECT_IN_PREPARATION = {"DK"}
# Ein Land ist Direkt-KANDIDAT, wenn das Register Dokumente per API herausgibt.
# Nur Daten per API reicht nicht -- dann bleibt der Bezug fuer Dokumente bestehen.
CANDIDATE_VERDICTS = {"direct_strong", "direct_good", "direct_contract"}

BAND2CLASS = {"Low": "A", "Medium": "B", "High": "C", "Premium": "D"}

REGION = {
    "EUROPA": ["AX", "AL", "AT", "BY", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE",
               "FO", "FI", "FR", "DE", "GI", "GR", "GL", "GG", "HU", "IS", "IE", "IM",
               "IT", "JE", "LV", "LI", "LU", "MT", "MD", "MC", "ME", "NL", "MK", "NO",
               "PL", "PT", "RO", "RU", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA",
               "GB"],
    "NAHER OSTEN & AFRIKA": ["AO", "BH", "BW", "DJ", "ET", "IR", "IQ", "IL", "JO", "KE",
                             "KW", "LS", "MA", "MU", "OM", "PS", "QA", "SA", "SN", "SC",
                             "ZA", "TN", "TR", "AE", "YE"],
    "ASIEN-PAZIFIK": ["AM", "AU", "AZ", "BN", "KH", "CN", "CX", "CC", "CK", "GE", "HK",
                      "HK-IRD", "IN", "ID", "JP", "KZ", "KG", "LA", "MY", "MV", "MH",
                      "MM", "NP", "NZ", "PK", "PG", "PH", "WS", "SG", "SB", "KR", "LK",
                      "TW", "TH", "TO", "UZ", "VU", "VN", "PF"],
    "AMERIKA": ["AR", "BR", "CA", "CL", "CO", "CR", "EC", "GP", "MQ", "MX", "PA", "PY",
                "PE", "PR", "TT", "US", "VI", "YT"],
    "FINANZ- UND OFFSHORE-PLAETZE": ["AW", "BS", "BZ", "BM", "VG", "KY", "CW", "VC"],
}
ISO2REGION = {c: r for r, cs in REGION.items() for c in cs}


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def price_bands():
    """Baender je Land. Quelle: knowyourcustomer.com Preisbandseite, Abruf 2026-07-30.
    Liegt als Seed im Scratchpad-Skript; hier als Datei erwartet, damit die Herkunft
    nachvollziehbar ist."""
    p = os.path.join(ROOT, "curation", "price_bands.json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    matrix = load("jurisdiction_matrix.json")
    regintel = load("curation/registry_intelligence.json")
    routing = load("curation/document_kinds_routing.json")["routes"]

    # ACHTUNG Doppelcodes: der Katalog fuehrt fuer HK ZWEI Eintraege — "HK CR"
    # (Companies Registry, das Gesellschaftsregister) und "HK IRD" (Steuerbehoerde),
    # beide unter dem Code HK. Ein naives dict ueberschreibt CR mit IRD und liefert
    # dann die Dokumentenliste der Steuerbehoerde. Genau das ist am 2026-07-30 einmal
    # passiert. Deshalb: erster Eintrag gewinnt, Kollisionen werden ausgewiesen.
    mat_by, dupes = {}, collections.defaultdict(list)
    for j in matrix["jurisdictions"]:
        c = j.get("code")
        if not c:
            continue
        dupes[c].append(j.get("name"))
        mat_by.setdefault(c, j)
    collisions = {c: ns for c, ns in dupes.items() if len(ns) > 1}

    ri_by = {r["jurisdiction"]: r for r in regintel if r.get("jurisdiction")}
    bands = price_bands()
    jur = (bands or {}).get("jurisdictions", {})
    # Anzeigename: deutscher Name aus der Banddatei, sonst Katalogname, sonst Code.
    name_by = {c: (jur.get(c, {}).get("de") or mat_by.get(c, {}).get("name") or c)
               for c in set(list(jur) + list(mat_by))}

    out = []
    w = out.append
    w("# Kundentabellen — ERZEUGT, nicht getippt\n")
    w("*Ausgabe von `scripts/build_customer_tables.py`. Jede Zahl unten ist abgeleitet.*")
    w("*Nicht von Hand bearbeiten — Aenderungen gehoeren in die Datendateien oder das Skript.*\n")

    # ── A · Anbindungsart je Jurisdiktion, drei Stufen ──────────────────────
    w("\n## A · Anbindungsart je Jurisdiktion (Folien 7 und 17)\n")
    w("Herleitung: *produktiv* und *in Vorbereitung* sind Projektzustand (im Skript benannt).")
    w("*Aussichtsreich* wird abgeleitet: `goDirect.verdict` in "
      f"{sorted(CANDIDATE_VERDICTS)} **und** `documentsViaApi == true`.")
    w("Liefert das Register nur Daten per API, bleibt der bisherige Bezug fuer Dokumente noetig —")
    w("das zaehlt ausdruecklich **nicht** als Kandidat.\n")

    tiers = collections.defaultdict(list)
    detail = []
    for c in STP15:
        ri = ri_by.get(c)
        v = (ri or {}).get("goDirect", {}).get("verdict")
        docs_api = (ri or {}).get("documentsViaApi")
        if c in DIRECT_PRODUCTIVE:
            tier = "produktiv"
        elif c in DIRECT_IN_PREPARATION:
            tier = "in Vorbereitung"
        elif ri is None:
            tier = "nicht erhoben"
        elif v in CANDIDATE_VERDICTS and docs_api:
            tier = "aussichtsreich"
        else:
            tier = "kein Direktweg absehbar"
        tiers[tier].append(c)
        detail.append((c, name_by.get(c, c), tier, v or "—", docs_api))

    w("| Markt | Stufe | goDirect | Dokumente per API |")
    w("|---|---|---|---|")
    for c, n, tier, v, da in detail:
        w(f"| {n} ({c}) | **{tier}** | `{v}` | {da} |")
    w("")
    for t in ["produktiv", "in Vorbereitung", "aussichtsreich",
              "kein Direktweg absehbar", "nicht erhoben"]:
        if tiers[t]:
            w(f"- **{t}** ({len(tiers[t])}): {', '.join(tiers[t])}")
    w(f"\nDeutschland ist zusaetzlich produktiv, zaehlt aber nicht zu den 15.")

    # ── B · Satzung im Vendor-Katalog ───────────────────────────────────────
    w("\n\n## B · Gesellschaftsvertrag im Bezugskatalog (Folien 10/11, Spalte 4)\n")
    w("Herleitung: Treffer auf Satzungs-Stichwoerter in `documentsMandatory` / "
      "`documentsNonMandatory` des Katalogs.")
    w("**Wichtig:** Das ist die *Kanalwahrheit*. Ob das Register die Satzung haelt, "
      "steht in der Evidenzdatei — beides ist getrennt zu lesen.\n")
    import re
    NEEDLE = re.compile(r"articles|association|constitut|statut|memorandum|charter|by-?law",
                        re.I)
    w("| Markt | Pflichtdokument | Zusatzdokument | abgeleitet |")
    w("|---|---|---|---|")
    for c in STP15:
        j = mat_by.get(c)
        if not j:
            w(f"| {name_by.get(c,c)} ({c}) | — | — | **nicht erhoben** |")
            continue
        m = [x for x in (j.get("documentsMandatory") or []) if NEEDLE.search(x)]
        n = [x for x in (j.get("documentsNonMandatory") or []) if NEEDLE.search(x)]
        sym = "●" if m else ("◐" if n else "?")
        note = ""
        if any("certified" in x.lower() for x in n):
            note = " · **beglaubigt**"
        w(f"| {name_by.get(c,c)} ({c}) | {'; '.join(m) or '—'} | {'; '.join(n) or '—'} "
          f"| **{sym}**{note} |")
    w("\n**Lies das nicht blind ab.** Fuer Belgien fuehrt der Katalog *Constitution* als "
      "**Pflicht**dokument, waehrend wir es gegenueber dem Anbieter als Zusatzdokument "
      "verhandeln. Ein Widerspruch dieser Art ist erst zu klaeren, bevor die Zelle gesetzt wird.")

    # ── C · Preisklassen ────────────────────────────────────────────────────
    if bands:
        w("\n\n## C · Preisklassen (Folien 15 und 16)\n")
        cls_by = {c: BAND2CLASS[v["band"]] for c, v in jur.items() if v.get("band") in BAND2CLASS}
        w(f"Erfasste Jurisdiktionen: **{len(cls_by)}**. "
          f"Verteilung: " + " · ".join(
              f"{k}={v}" for k, v in sorted(collections.Counter(cls_by.values()).items())))
        n_low_med = sum(1 for c in STP15 if cls_by.get(c) in ("A", "B"))
        w(f"\nVon den 15 Maerkten liegen **{n_low_med}** in den Klassen A und B, "
          f"**{15 - n_low_med}** darueber.")
        w("\n### Die 15 Maerkte\n")
        w("| Markt | Klasse | Anbindung |")
        w("|---|---|---|")
        for c in STP15:
            tier = next(t for t, cs in tiers.items() if c in cs)
            mark = "**direkt**" if c in DIRECT_PRODUCTIVE else (
                "direkt i. V." if c in DIRECT_IN_PREPARATION else "indirekt")
            w(f"| {name_by.get(c,c)} | **{cls_by.get(c,'?')}** | {mark} |")
        w("\n*Die Klasse beschreibt den Preis der **indirekten** Anbindung. "
          "Fuer die Direktlaender gilt sie nicht — dort zaehlen die eigenen Betraege.*")

        w("\n### Alle Jurisdiktionen nach Region und Klasse\n")
        unknown = [c for c in cls_by if not jur.get(c, {}).get("region")]
        regions = sorted({v["region"] for v in jur.values() if v.get("region")})
        for region in regions:
            members = sorted((c for c in cls_by if jur.get(c, {}).get("region") == region),
                             key=lambda c: (cls_by[c], name_by.get(c, c)))
            if not members:
                continue
            w(f"\n**{region}** ({len(members)})\n")
            byc = collections.defaultdict(list)
            for c in members:
                byc[cls_by[c]].append(name_by.get(c, c))
            for k in "ABCD":
                if byc[k]:
                    w(f"- **{k}** — {', '.join(sorted(byc[k]))}")
        if unknown:
            w(f"\n**OHNE REGIONSZUORDNUNG ({len(unknown)}): {', '.join(sorted(unknown))}** "
              "— im Skript ergaenzen, sonst fehlen sie in der Folie.")
    else:
        w("\n\n## C · Preisklassen — UEBERSPRUNGEN\n")
        w("`curation/price_bands.json` fehlt. Ohne diese Datei werden keine Klassen erzeugt, "
          "damit niemand sie von Hand eintippt.")

    # ── D · Selbstpruefung ──────────────────────────────────────────────────
    if collisions:
        w("\n\n### Doppelt vergebene Laendercodes im Katalog\n")
        w("Erster Eintrag wurde verwendet. Wer hier den falschen erwischt, liest die "
          "Dokumentenliste eines anderen Registers.\n")
        for c, ns in sorted(collisions.items()):
            w(f"- `{c}` — " + " · ".join(f"**{n}**" if i == 0 else str(n)
                                         for i, n in enumerate(ns))
              + "  (verwendet: der erste)")

    w("\n\n## D · Selbstpruefung\n")
    kinds = ["REGISTERAUSZUG", "GESELLSCHAFTSVERTRAG", "GESELLSCHAFTERLISTE"]
    rby = collections.defaultdict(list)
    for r in routing:
        rby[r["jurisdiction"]].append(r)
    gaps = []
    for c in STP15:
        rs = rby.get(c, [])
        if not rs:
            gaps.append(f"**{c}: keine einzige Routenzeile** — jede Aussage ueber {c} ist ungedeckt")
            continue
        missing = [k for k in kinds if not any(r["kind"] == k for r in rs)]
        if missing:
            gaps.append(f"{c}: keine Zeilen fuer {', '.join(missing)}")
    if gaps:
        w("**Luecken im Datenbestand — Aussagen dazu sind NICHT gedeckt:**\n")
        for g in gaps:
            w(f"- {g}")
    else:
        w("Keine Luecken: alle 15 Maerkte haben Zeilen fuer alle drei Dokumentenarten.")

    dest = os.path.join(ROOT, "docs", "generated")
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, "customer_tables.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"\n\n-> geschrieben: {path}")


if __name__ == "__main__":
    main()
