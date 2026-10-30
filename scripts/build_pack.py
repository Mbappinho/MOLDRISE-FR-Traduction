"""Build the official FR language pack (Steam 1.2+) from work/tr_steam/*.json.

Output: build/translations/fr/{*.csv, pack.cfg}
Usage : python scripts/build_pack.py [--check] [--install] [--no-en]
  --install : copy the pack to %APPDATA%/Raffa/MOLDRISE_FULL/translations/fr
  --no-en   : write keys,fr only (distribution without the game's English text)
"""
import csv, importlib.util, json, os, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "work/tr_steam"
OUT = ROOT / "build/translations/fr"
spec = importlib.util.spec_from_file_location("build_mod", ROOT / "scripts/build_mod.py")
bm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bm)

PH = re.compile(r"%[-+0-9.]*[sdif]|\{[a-zA-Z_0-9]*\}")
TAG = re.compile(r"\[/?([a-z_]+)[^\]]*\]")
VERSION = "1.0.2"


def tokens(s):
    return sorted(bm.TOKEN.findall(s))


def main():
    check = "--check" in sys.argv
    no_en = "--no-en" in sys.argv
    errors, stats = [], {"files": 0, "rows": 0, "translated": 0, "todo": 0}
    if not check:
        shutil.rmtree(OUT, ignore_errors=True)
        OUT.mkdir(parents=True)
    for p in sorted(SRC.glob("*.json")):
        data = json.loads(p.read_text("utf-8"))
        rows = []
        for key, e in data.items():
            fr = bm.typo(e["fr"]) if e.get("fr") else ""
            stats["rows"] += 1
            if fr:
                stats["translated"] += 1
                if tokens(e["en"]) != tokens(fr):
                    errors.append(f"{p.stem}/{key}: tokens EN {tokens(e['en'])} != FR {tokens(fr)}")
            else:
                stats["todo"] += 1
            rows.append([key, fr] if no_en else [key, e["en"], fr])
        stats["files"] += 1
        if not check:
            with open(OUT / f"{p.stem}.csv", "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["keys", "fr"] if no_en else ["keys", "en", "fr"])
                w.writerows(rows)
    if not check:
        (OUT / "pack.cfg").write_text(
            '[pack]\n\nlocale="fr"\nname="Français"\nauthor="Mbappinho"\n'
            f'version="{VERSION}"\noverride=false\n', "utf-8")
    for e in errors:
        print("QA", e)
    print(("check " if check else "built ") + json.dumps(stats), f"errors={len(errors)}")
    if "--install" in sys.argv and not check:
        dst = pathlib.Path(os.environ["APPDATA"]) / "Raffa/MOLDRISE_FULL/translations/fr"
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(OUT, dst)
        print("installed ->", dst)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
