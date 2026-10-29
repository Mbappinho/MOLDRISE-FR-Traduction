"""Port the FR translation to the game's official language-pack system (Steam 1.2+).

Input : work/starter_pack_fr/*.csv  (generated in-game by TranslationPackExporter.write_starter_pack("fr"); keys,en,fr)
        build/MOLDRISE_FR/fr_data.json (our v1.0.2 translation, typography already applied)
Output: work/tr_steam/<file>.json   {key: {"en": ..., "fr": ..., "src": exact|same_file|elsewhere|fuzzy|todo, ("old_en": ...)}}
        Existing work/tr_steam entries whose EN is unchanged are kept (they are the new source of truth).

Usage: python scripts/steam_port.py            # (re)build work/tr_steam from starter + old data
"""
import csv, difflib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
STARTER = ROOT / "work/starter_pack_fr"
OUT = ROOT / "work/tr_steam"
OUT.mkdir(parents=True, exist_ok=True)
old = json.loads((ROOT / "build/MOLDRISE_FR/fr_data.json").read_text("utf-8"))


def norm(s: str) -> str:
    return s.replace("\u2019", "'").replace("\u2026", "...").replace("\r", "").strip()


def read_csv(p):
    with open(p, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return [(r[0], r[1]) for r in rows[1:] if r and r[0]]


# global EN -> FR lookups
glob_dialog = {}
for fname, entries in old["dialogs"].items():
    for k, (en, fr) in entries.items():
        glob_dialog.setdefault(norm(en), fr)
ui = {norm(en): fr for en, fr in old["ui"].items()}
chars = {}
for c, d in old["chars"].items():
    for prop, (en, fr) in d.items():
        chars[norm(en)] = fr

stats = {}
for p in sorted(STARTER.glob("*.csv")):
    name = p.stem
    rows = read_csv(p)
    prev_path = OUT / f"{name}.json"
    prev = json.loads(prev_path.read_text("utf-8")) if prev_path.exists() else {}
    out = {}
    if name.startswith("dialog_"):
        mine = old["dialogs"].get(name, {})
        prefix = "D_" + name[len("dialog_"):].upper() + "_"
        same_file_by_en = {norm(en): fr for en, fr in mine.values()}
        old_keys = {k: (en, fr) for k, (en, fr) in mine.items()}
    for key, en in rows:
        if key in prev and prev[key]["en"] == en and prev[key].get("fr"):
            out[key] = prev[key]
            continue
        e = {"en": en, "fr": "", "src": "todo"}
        n = norm(en)
        if name.startswith("dialog_"):
            short = key[len(prefix):] if key.startswith(prefix) else key
            if short in old_keys and norm(old_keys[short][0]) == n:
                e.update(fr=old_keys[short][1], src="exact")
            elif n in same_file_by_en:
                e.update(fr=same_file_by_en[n], src="same_file")
            elif n in glob_dialog:
                e.update(fr=glob_dialog[n], src="elsewhere")
            elif short in old_keys and difflib.SequenceMatcher(None, norm(old_keys[short][0]), n).ratio() > 0.8:
                e.update(fr=old_keys[short][1], src="fuzzy", old_en=old_keys[short][0])
        elif name == "characters":
            if n in chars:
                e.update(fr=chars[n], src="exact")
        else:
            if n in ui:
                e.update(fr=ui[n], src="exact")
        out[key] = e
    prev_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), "utf-8")
    s = {}
    for e in out.values():
        s[e["src"]] = s.get(e["src"], 0) + 1
    stats[name] = s
tot = {}
for s in stats.values():
    for k, v in s.items():
        tot[k] = tot.get(k, 0) + v
for n, s in stats.items():
    print(f"{n:28} {s}")
print("TOTAL", tot)
