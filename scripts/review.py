"""Independent review of FR translations by Gemini (different model family than the translator).

Usage:
  python scripts/review.py dialog dialog_old_lady
  python scripts/review.py ui            # UI + Const strings, chunked
Output: work/review/<name>.json  (findings only; never auto-applied — triaged by the translator, validated by Théo)
"""
import json, pathlib, re, subprocess, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gemini  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
TR = ROOT / "work/tr"
OUT = ROOT / "work/review"
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash"]  # free-tier quotas are per model
GUIDE = (ROOT / "docs/GUIDE_TRADUCTION.md").read_text("utf-8")

SYSTEM = f"""Tu es relecteur professionnel de localisation de jeux vidéo, EN -> FR (France).
Tu relis une traduction faite par quelqu'un d'autre. Sois exigeant mais juste : ne signale que de vrais problèmes,
pas des préférences personnelles. Une traduction correcte et naturelle ne doit PAS être signalée.

Critères (catégories) :
- sens : contresens, faux-sens, omission, ajout, nuance perdue
- registre : tu/vous incohérent avec le guide ou avec le reste du personnage, niveau de langue inadapté
- ton : la voix du personnage ou l'humour/horreur n'est pas rendu, jurons atténués ou exagérés
- naturel : calque de l'anglais, tournure non idiomatique, formulation lourde
- glossaire : terme non conforme au glossaire, incohérence de terminologie
- langue : faute d'orthographe, grammaire, accord, conjugaison
- technique : balises BBCode, expressions {{...}}, %s/%d, retours à la ligne modifiés (rare, déjà vérifié par script)

Sévérité : P0 = bloquant/contresens ; P1 = erreur nette à corriger ; P2 = amélioration nettement meilleure.
Pour chaque problème, donne une suggestion FR complète prête à remplacer le texte FR entier.
Les espaces insécables avant ! ? : ; sont ajoutées automatiquement au build : ne les signale pas.

GUIDE DE TRADUCTION DU PROJET (fait foi) :
{GUIDE}

Réponds UNIQUEMENT en JSON :
{{"findings": [{{"id": "...", "severity": "P0|P1|P2", "category": "...", "issue": "explication courte en français", "suggestion": "texte FR complet corrigé"}}],
  "summary": "2-3 phrases d'appréciation globale"}}"""


def dialog_entries(name):
    tr = json.loads((TR / "dialogs" / f"{name}.json").read_text("utf-8"))
    dump = subprocess.run([sys.executable, str(ROOT / "scripts/dump_dialog.py"), name],
                          capture_output=True, text=True, encoding="utf-8").stdout
    order, entries = [], []
    for line in dump.splitlines():
        m = re.match(r"\s*(->)?\s*([A-Z0-9_]+) \| (?:\[([^\]]*)\] )?", line)
        if m and m.group(2) in tr and m.group(2) not in order:
            order.append(m.group(2))
            speaker = "JOUEUR (choix de réponse)" if m.group(1) else (m.group(3) or "?")
            e = tr[m.group(2)]
            entries.append({"id": m.group(2), "speaker": speaker, "en": e["en"], "fr": e["fr"], **({"note": e["note"]} if e.get("note") else {})})
    for k, e in tr.items():
        if k not in order:
            entries.append({"id": k, "speaker": "?", "en": e["en"], "fr": e["fr"]})
    return entries


def ui_entries():
    todo = {i["id"]: i for i in json.loads((TR / "ui_todo.json").read_text("utf-8"))}
    out = []
    for src in ("ui_fr.json", "ui_fr_const.json"):
        for k, fr in json.loads((TR / src).read_text("utf-8")).items():
            en = k[3:] if k.startswith("en:") else todo[k]["en"]
            ctx = "" if k.startswith("en:") else todo[k]["file"]
            out.append({"id": k, "context": ctx, "en": en, "fr": fr})
    return out


def ask(user):
    """Try each free model in turn; a 429 (daily quota) on one model falls through to the next."""
    last = None
    for m in MODELS:
        try:
            text, usage = gemini.generate(m, SYSTEM, user, retries=2)
            return m, text, usage
        except SystemExit as e:
            last = e
            print(f"  {m} failed: {str(e)[:120]}")
    raise SystemExit(f"all models failed: {last}")


def run(name, entries, intro, chunk=200):
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / f"{name}.json").exists() and "--force" not in sys.argv:
        print(name, "already reviewed, skip (use --force)")
        return
    findings, summaries, used = [], [], set()
    for i in range(0, len(entries), chunk):
        part = entries[i:i + chunk]
        user = intro + "\n\nENTRÉES :\n" + json.dumps(part, ensure_ascii=False, indent=0)
        t = time.time()
        model, text, usage = ask(user)
        used.add(model)
        data = json.loads(text)
        findings += data.get("findings", [])
        summaries.append(data.get("summary", ""))
        print(f"{name} chunk {i // chunk + 1}: {len(data.get('findings', []))} findings, {usage.get('totalTokenCount')} tok, {time.time() - t:.0f}s")
        time.sleep(7)
    known = {e["id"]: e for e in entries}
    for f in findings:
        if f.get("id") in known:
            f["en"], f["fr"] = known[f["id"]]["en"], known[f["id"]]["fr"]
    res = {"model": sorted(used), "name": name, "count": len(entries), "findings": findings, "summary": summaries}
    (OUT / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), "utf-8")
    sev = {s: sum(f.get("severity") == s for f in findings) for s in ("P0", "P1", "P2")}
    print(name, sev, "->", OUT / f"{name}.json")


if __name__ == "__main__":
    kind = sys.argv[1]
    if kind == "all":
        for f in sorted((TR / "dialogs").glob("*.json")):
            try:
                run(f.stem, dialog_entries(f.stem),
                    f"Fichier de dialogue '{f.stem}' du jeu MOLDRISE, dans l'ordre de la conversation. "
                    "'speaker' indique qui parle ; les répliques JOUEUR sont des choix de réponse.")
            except SystemExit as e:
                print(f.stem, "STOPPED:", e)
                break
    elif kind == "dialog":
        name = sys.argv[2]
        run(name, dialog_entries(name),
            f"Fichier de dialogue '{name}' du jeu MOLDRISE, dans l'ordre de la conversation. "
            "'speaker' indique qui parle ; les répliques JOUEUR sont des choix de réponse.")
    elif kind == "ui":
        run("ui", ui_entries(),
            "Textes d'interface, objets, Idées, messages de mort, voix intérieure de l'infection (jeu MOLDRISE). "
            "'context' = fichier source (ex. Settings.tscn, Player.gd, Const.gd). Les textes courts sont des boutons/labels : la concision compte.")
