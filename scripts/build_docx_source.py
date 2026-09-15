# -*- coding: utf-8 -*-
"""Produce a Word-friendly HTML of the Septeo pack, for conversion to .docx.

Why this exists: the contract is laid out as fixed-width A4 pages with CSS, and
the internal notes are hidden from print with @media print. **Word does not
honour @media print.** Converting the contract HTML directly would hand the
counterparty our internal commentary. This script removes those blocks
structurally and flattens the page chrome into a plain document flow that
redlines cleanly in Word.

    python scripts/build_docx_source.py            # writes build/*.docx.html
    python scripts/build_docx_source.py --check    # verify no internal content

Then convert with scripts/to_docx.ps1.
"""
from __future__ import print_function

import argparse
import io
import os
import re
import sys

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DOCS = os.path.join(REPO, "docs")
BUILD = os.path.join(REPO, "build")

SOURCES = [
    ("SEPTEO_RESELLER_AGREEMENT_2026-09-14.html", "Reseller Agreement"),
]

# Anything matching these is internal and must never reach the .docx.
INTERNAL_MARKERS = [
    "internal", "Internal note", "not printed", "not part of the Agreement",
]

WORD_CSS = u"""
  body { font-family:"Calibri","Segoe UI",sans-serif; font-size:10.5pt; color:#222233;
         line-height:1.35; }
  h1 { font-family:"Calibri",sans-serif; font-size:19pt; color:#1a2340; margin:0 0 4pt; }
  h2 { font-family:"Calibri",sans-serif; font-size:12pt; color:#1a2340;
       margin:16pt 0 6pt; border-bottom:1pt solid #6895FF; padding-bottom:2pt; }
  h3 { font-size:11pt; color:#1a2340; margin:12pt 0 4pt; }
  p  { margin:0 0 6pt; }
  p.cl { margin:0 0 6pt; }
  p.kicker { color:#6895FF; font-size:8pt; letter-spacing:1pt; margin:0 0 2pt; }
  p.meta { font-size:9pt; color:#6b7280; margin:0 0 3pt; }
  table { border-collapse:collapse; width:100%; font-size:9.5pt; margin:6pt 0 10pt; }
  th { background:#1a2340; color:#ffffff; text-align:left; padding:4pt 6pt;
       font-size:8pt; }
  td { border-bottom:0.5pt solid #e5e7eb; padding:4pt 6pt; vertical-align:top; }
  ul, ol { margin:0 0 8pt 18pt; padding:0; }
  li { margin:0 0 4pt; }
  .pagebreak { page-break-before:always; }
"""


def is_internal(tag):
    classes = tag.get("class") or []
    if any("internal" in c for c in classes):
        return True
    return False


def clean(path, title):
    soup = BeautifulSoup(io.open(path, encoding="utf-8").read(), "lxml")

    # 1. remove internal blocks, structurally.
    # Collect first: decomposing while iterating detaches descendants and the
    # walk then trips over them, which would abort mid-strip -- the one failure
    # mode that could leave internal text in the output.
    doomed = [t for t in soup.find_all(True) if is_internal(t)]
    doomed += soup.find_all("style")
    removed = 0
    for tag in doomed:
        if tag.decomposed:
            continue
        tag.decompose()
        removed += 1

    out = BeautifulSoup(
        u"<html><head><meta charset='utf-8'><title>%s</title>"
        u"<style>%s</style></head><body></body></html>" % (title, WORD_CSS),
        "lxml")
    body = out.body

    def add(tag_name, text=None, cls=None, node=None):
        el = out.new_tag(tag_name)
        if cls:
            el["class"] = cls
        if node is not None:
            el.append(BeautifulSoup(node.decode_contents(), "lxml"))
        elif text:
            el.string = text
        body.append(el)
        return el

    first_page = True
    for page in soup.find_all("div", class_="page"):
        if not first_page:
            br = out.new_tag("p")
            br["class"] = "pagebreak"
            br.string = u" "
            body.append(br)
        first_page = False

        hdr = page.find("div", class_="doc-header")
        if hdr:
            k = hdr.find("div", class_="kicker")
            if k:
                add("p", k.get_text(" ", strip=True), cls="kicker")
            h1 = hdr.find("h1")
            if h1:
                add("h1", h1.get_text(" ", strip=True))

        for meta in page.find_all("div", class_=["doc-meta", "party-line", "doc-date"]):
            for chunk in meta.stripped_strings:
                add("p", chunk, cls="meta")

        lead = page.find("p", class_="lead")
        if lead:
            add("p", node=lead)

        for sec in page.find_all("div", class_="section"):
            h2 = sec.find("h2")
            if h2:
                add("h2", h2.get_text(" ", strip=True))
            for child in sec.find_all(["p", "table", "ul", "ol", "dl"], recursive=True):
                if child.find_parent("table") or child.find_parent(["ul", "ol", "dl"]):
                    continue
                if child.name == "p" and child.find_parent("div", class_="cl"):
                    continue
                body.append(BeautifulSoup(child.decode(), "lxml").find(child.name))
            # clause rows: number and text as one paragraph, which redlines well
            for cl in sec.find_all("div", class_="cl"):
                num = cl.find("span", class_="n")
                para = cl.find("p")
                if para is None:
                    dl = cl.find("dl")
                    if dl:
                        body.append(BeautifulSoup(dl.decode(), "lxml").find("dl"))
                    continue
                n = num.get_text(strip=True) if num else ""
                el = out.new_tag("p")
                el["class"] = "cl"
                if n:
                    b = out.new_tag("b")
                    b.string = n + " "
                    el.append(b)
                el.append(BeautifulSoup(para.decode_contents(), "lxml"))
                body.append(el)

        sig = page.find("div", class_="sig-grid")
        if sig:
            add("h2", "Signatures")
            for blk in sig.find_all("div", class_="sig-block"):
                name = blk.find("h4")
                add("p", (name.get_text(strip=True) if name else ""))
                add("p", u" ")
                add("p", u"_________________________________")
                cap = blk.find("div", class_="sig-label")
                add("p", cap.get_text(" ", strip=True) if cap else "", cls="meta")

    # chips (Annex 2.2) become a plain comma list: 153 inline-flex spans are
    # unreadable in Word and impossible to redline
    for chips in body.find_all("div", class_="chips"):
        names = [c.get_text(" ", strip=True) for c in chips.find_all("span")]
        p = out.new_tag("p")
        p.string = u", ".join(names)
        chips.replace_with(p)

    html = out.decode()
    return html, removed


def verify(html, label):
    txt = BeautifulSoup(html, "lxml").get_text(" ", strip=True)
    bad = [m for m in INTERNAL_MARKERS if m.lower() in txt.lower()]
    if bad:
        raise SystemExit("REFUSING: internal content survived in %s: %s" % (label, bad))
    return len(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(BUILD):
        os.makedirs(BUILD)

    for fname, title in SOURCES:
        src = os.path.join(DOCS, fname)
        if not os.path.exists(src):
            print("skip (missing):", fname)
            continue
        html, removed = clean(src, title)
        chars = verify(html, fname)
        dest = os.path.join(BUILD, fname.replace(".html", ".docx.html"))
        if not args.check:
            io.open(dest, "w", encoding="utf-8").write(html)
        print("%-46s internal blocks removed: %d   text: %d chars   -> %s"
              % (fname, removed, chars, os.path.basename(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
