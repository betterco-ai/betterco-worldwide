"""Generate the backend's document-role resource from the hand-authored curation.

The curation is the source of truth and stays here, where it is maintained. This emits the shape the
Java side reads, so the mapping is never re-authored by hand in two languages.

    python scripts/build_document_roles.py

Only `via: "document"` rows can map a delivered file to a role. A `via: "data"` row means the
jurisdiction answers that question with data fields rather than a document - real, and nothing a
stored PDF can satisfy.
"""
import json, io, os, re, collections

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURATION = os.path.join(HERE, "curation", "document_kinds_curation.json")
TARGET = os.path.join(os.path.dirname(os.path.dirname(HERE)), "betterco-backend", "betterco-backend",
                      "src", "main", "resources", "kyc", "document-roles.json")


def norm(s):
    """Match the API's spelling to the matrix's: case, &/and, stray punctuation."""
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower().replace("&", "and")).strip()


rows = json.load(io.open(CURATION, encoding="utf-8"))
out = collections.defaultdict(lambda: collections.defaultdict(list))
skipped_data = 0
for r in rows:
    if r.get("via") != "document" or not r.get("label"):
        skipped_data += 1
        continue
    kinds = out[r["jurisdiction"]][norm(r["label"])]
    if r["kind"] not in kinds:
        kinds.append(r["kind"])

result = {j: dict(labels) for j, labels in sorted(out.items())}
os.makedirs(os.path.dirname(TARGET), exist_ok=True)
io.open(TARGET, "w", encoding="utf-8", newline="\n").write(json.dumps(result, indent=1, sort_keys=True) + "\n")
multi = sum(1 for j in result.values() for k in j.values() if len(k) > 1)
print("wrote %s" % TARGET)
print("  %d jurisdictions, %d labels, %d of them playing more than one role, %d data-only rows skipped"
      % (len(result), sum(len(v) for v in result.values()), multi, skipped_data))
print("  GB:", json.dumps(result.get("GB")))
