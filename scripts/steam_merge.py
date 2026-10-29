"""Merge sub-agent drafts (work/tr_steam_drafts/<file>.json = {key: fr}) into work/tr_steam/<file>.json.

Merged entries get src="new" (was todo) or src="updated" (was fuzzy/other); old_en is dropped once updated.
Usage: python scripts/steam_merge.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
total = 0
for d in sorted((ROOT / "work/tr_steam_drafts").glob("*.json")):
    tgt = ROOT / "work/tr_steam" / d.name
    data = json.loads(tgt.read_text("utf-8"))
    draft = json.loads(d.read_text("utf-8"))
    unknown = [k for k in draft if k not in data]
    n = 0
    for k, fr in draft.items():
        if k not in data:
            continue
        e = data[k]
        if e.get("fr") == fr and e["src"] not in ("todo", "fuzzy"):
            continue
        e["src"] = "new" if e["src"] == "todo" else "updated"
        e["fr"] = fr
        e.pop("old_en", None)
        n += 1
    tgt.write_text(json.dumps(data, ensure_ascii=False, indent=1), "utf-8")
    left = [k for k, e in data.items() if e["src"] in ("todo", "fuzzy") and e["en"]]
    print(f"{d.stem:28} merged {n:4}  unknown {unknown}  still todo/fuzzy {len(left)}")
    total += n
print("total merged", total)
