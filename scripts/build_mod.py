"""Build the distributable mod folder from work/tr/* translation sources.

Output: build/MOLDRISE_FR/{fr_mod.gd, fr_data.json, textures/*} + build/override.cfg
Exit code 1 if QA errors (broken tags/placeholders, stale EN sources).
"""
import json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TR = ROOT / "work" / "tr"
OUT = ROOT / "build"
MOD = OUT / "MOLDRISE_FR"

BBCODE = r"(?:b|i|u|s|code|center|left|right|fill|indent|url|img|font|font_size|color|bgcolor|fgcolor|outline_size|outline_color|shake|wave|tornado|rainbow|fade|pulse|quest|ghost|hint|table|cell|ul|ol|lb|rb)"
TOKEN = re.compile(r"\[/?" + BBCODE + r"(?:[ =][^\]]*)?\]|\{[^}]+\}|%[-0-9.]*[sdf]")
NBSP = "\u00a0"


def load(p, default):
    return json.loads(p.read_text("utf-8")) if p.exists() else default


def typo(s: str) -> str:
    """French typography with the only no-break space the game fonts support (U+00A0)."""
    s = s.replace("\u202f", NBSP)
    s = re.sub(r" ([!?:;»])", NBSP + r"\1", s)
    s = re.sub(r"« ", "«" + NBSP, s)
    # undo inside BBCode tags / code expressions, e.g. [font size=60] or {A.b()}
    s = TOKEN.sub(lambda m: m.group(0).replace(NBSP, " "), s)
    return s


def qa(where, en, fr, errors):
    def toks(s):
        return sorted(t for t in TOKEN.findall(s) if not t.startswith("[/"))
    if toks(en) != toks(fr):
        errors.append(f"{where}: tokens differ\n    EN {toks(en)}\n    FR {toks(fr)}")
    if en.count("\n") != fr.count("\n"):
        errors.append(f"{where}: line count differs ({en.count(chr(10))} vs {fr.count(chr(10))})")


def unesc(s):
    """inventory keeps .tres escaping (\\" and \\\\); the game sees the unescaped string."""
    return re.sub(r'\\(.)', r'\1', s)


def build_ui(errors):
    todo = {i["id"]: i["en"] for i in load(TR / "ui_todo.json", [])}
    ui = {}
    for src in ("ui_fr.json", "ui_fr_const.json"):
        for k, fr in load(TR / src, {}).items():
            en = k[3:] if k.startswith("en:") else todo.get(k)
            if en is None:
                errors.append(f"{src}: unknown id {k}")
                continue
            qa(f"ui {k}", en, fr, errors)
            ui[en] = typo(fr)
    return ui


def main():
    check_only = "--check" in sys.argv  # QA only, writes nothing (safe for parallel translators)
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None)
    if not check_only:
        if MOD.exists():
            shutil.rmtree(MOD)
        (MOD / "textures").mkdir(parents=True)
    inv = json.loads((ROOT / "work" / "inventory_en.json").read_text("utf-8"))
    inv_dialog = {(i["file"], i["key"]): i["en"] for i in inv if i["kind"] in ("dialog", "option")}

    errors = []
    data = {"ui": build_ui(errors), "dialogs": {}, "chars": {}, "textures": {}, "patterns": {}}
    for f in sorted((TR / "dialogs").glob("*.json")) if (TR / "dialogs").exists() else []:
        if only and f.stem != only:
            continue
        out = {}
        for key, e in load(f, {}).items():
            if not e.get("fr"):
                continue
            src = inv_dialog.get((f.stem, key))
            if src is None or src != e["en"]:
                errors.append(f"{f.stem}/{key}: EN source differs from current inventory")
                continue
            qa(f"{f.stem}/{key}", e["en"], e["fr"], errors)
            out[key] = [unesc(e["en"]), unesc(typo(e["fr"]))]
        if out:
            data["dialogs"][f.stem] = out
    for file, fields in load(TR / "chars.json", {}).items():
        data["chars"][file] = {k: [v["en"], typo(v["fr"])] for k, v in fields.items() if v.get("fr")}
    for res_path, rel in load(TR / "textures.json", {}).items():
        src = TR / "textures" / rel
        if not src.exists():
            errors.append(f"texture missing: {src}")
            continue
        if not check_only:
            shutil.copy2(src, MOD / "textures" / rel)
        data["textures"][res_path] = f"textures/{rel}"
    pat = load(TR / "patterns.json", {})
    pat.pop("_doc", None)
    for r in pat.get("full", []) + pat.get("sub", []):
        r["fr"] = typo(r["fr"])
    data["patterns"] = pat
    data["layout"] = [{k: v for k, v in r.items() if not k.startswith("_")} for r in load(TR / "layout.json", [])]

    if check_only:
        for e in errors:
            print("QA", e)
        print("check", "FAIL" if errors else "OK", {k: sum(len(v) for v in data["dialogs"].values()) for k in ["dialogs"]})
        return 1 if errors else 0
    (MOD / "fr_data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), "utf-8")
    shutil.copy2(ROOT / "mod" / "fr_mod.gd", MOD / "fr_mod.gd")
    # Godot resolves res:// paths missing from the pck against the exe directory -> relative path is portable.
    (OUT / "override.cfg").write_text('[autoload]\n\nFrMod="*res://MOLDRISE_FR/fr_mod.gd"\n', "utf-8")
    counts = {k: (sum(len(v) for v in data[k].values()) if k == "dialogs" else len(data[k])) for k in data if k != "patterns"}
    print("built", counts)
    for e in errors:
        print("QA", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
