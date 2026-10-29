"""Independent Gemini review of everything added/changed for the Steam 1.2 port (src new|updated in work/tr_steam).

Usage: python scripts/review_steam.py [--force]
Output: work/review/steam_<file>.json (findings only; triaged by the translator, validated by Théo)
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import review  # noqa: E402  (reuses SYSTEM prompt, model fallback and chunked run)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CTX = 40

only = [a for a in sys.argv[1:] if not a.startswith("--")]
for p in sorted((ROOT / "work/tr_steam").glob("*.json")):
    if only and p.stem not in only:
        continue
    data = json.loads(p.read_text("utf-8"))
    keys = list(data)
    targets = [k for k in keys if data[k]["src"] in ("new", "updated") and data[k]["en"]]
    if not targets:
        continue
    entries = [{"id": k, "en": data[k]["en"], "fr": data[k]["fr"]} for k in targets]
    # context: already-reviewed lines of the same file, nearest to the targets, for tone / tu-vous / terms
    tset = set(targets)
    near = []
    for k in targets:
        i = keys.index(k)
        for j in range(max(0, i - 2), min(len(keys), i + 3)):
            if keys[j] not in tset and keys[j] not in near:
                near.append(keys[j])
    ctx = [{"id": k, "en": data[k]["en"], "fr": data[k]["fr"]} for k in near[:CTX]]
    kind = "fichier de dialogue" if p.stem.startswith("dialog_") else "textes d'interface/objets/succès"
    intro = (
        f"Jeu MOLDRISE, {kind} '{p.stem}'. Les ENTRÉES sont des traductions NOUVELLES ou MODIFIÉES "
        "pour la dernière version du jeu : ce sont elles seules que tu relis. Les clés suivent l'ordre du jeu "
        "(START_DIALOG_n = réplique du PNJ, START_OPT = choix du joueur ; préfixes = branches). "
        "Ne signale RIEN dans le CONTEXTE ci-dessous (déjà validé) ; utilise-le pour vérifier la cohérence "
        "de ton, du tu/vous et des termes.\n\nCONTEXTE (déjà validé, ne pas relire) :\n"
        + json.dumps(ctx, ensure_ascii=False, indent=0)
    )
    review.run(f"steam_{p.stem}", entries, intro, chunk=120)
