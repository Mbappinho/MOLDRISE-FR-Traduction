# MOLDRISE FR — Notes de développement

> Document technique. Pour installer la traduction, voir le [README](../README.md).

Fan patch FR non officiel pour *MOLDRISE* (Godot 4.7, Steam AppID `4519130`).

## Statut (Steam 1.2, build 25670818)

Le jeu embarque désormais un système officiel de packs de langue : il charge `%APPDATA%/Raffa/MOLDRISE_FULL/translations/<locale>/` (`pack.cfg` + CSV `keys,en,fr`).
**Plus aucun mod ni injection** : la VF est un simple pack `fr`, sélectionnable dans Paramètres > Langue.

- Source de vérité : `work/tr_steam/*.json` (clé officielle → en/fr/src).
- Build : `python scripts/build_pack.py [--install] [--no-en]` → `build/translations/fr/`.
- Après une mise à jour du jeu : régénérer le starter pack en jeu (`TranslationPackExporter.write_starter_pack("fr")`), puis `scripts/steam_port.py` (conserve les entrées dont l'anglais n'a pas bougé, marque `todo`/`fuzzy` le reste) → `scripts/steam_merge.py`.
- Couverture : 2 257 / 2 258 entrées (la dernière est vide en anglais). Les 20 dialogues ont été testés en jeu en FR sans plantage ni anglais visible.
- L'ancien mod runtime (`mod/`, `scripts/build_mod.py`) reste pour la v1.0.2 uniquement.

## Dépôt public / privé

Le dépôt public (`Mbappinho/MOLDRISE-FR-Traduction`) ne contient **aucun texte anglais du jeu** : seulement le pack `translations/fr/` (colonnes `keys,fr`), la doc et les scripts.
Les fichiers de travail (`work/tr_steam`, qui contient l'anglais pour détecter les changements après un patch) restent privés.
Synchronisation : `python scripts/publish_public.py <clone_public>`.

## Historique : mod runtime pour la v1.0.2 (obsolète)

Tout ce qui suit décrit la première méthode (injection au runtime), écrite pour la v1.0.2 avant que le jeu ait son propre système de langues. Elle est conservée pour mémoire.

### État

| | |
|--|--|
| Version jeu de travail | v1.0.2 — BuildID `24334866` (hashes : `work/game_hashes_v1.0.2_build24334866.txt`) |
| Méthode | Injection au runtime, **aucun fichier du jeu modifié**. Validée en jeu le 2026-10-28. |
| Traduit | **Tout le texte du jeu** : interface (532), 19 fichiers de dialogue (1 406 répliques), 18 persos. Relu par Gemini sauf les 2 distributeurs (quota). |
| À faire | Relecture des 2 distributeurs · ~20 textures · bandeau vidéo de fin · **validation par Théo** · test sur la version Steam |

### Installation (test)

```
python scripts/build_mod.py      # -> build/MOLDRISE_FR/ + build/override.cfg
```
Copier `build/MOLDRISE_FR/` et `build/override.cfg` à côté de `MOLDRISE.exe`.
Pour désinstaller : supprimer ces deux éléments.
Debug : créer `MOLDRISE_FR/debug.txt` → `%APPDATA%/Raffa/MOLDRISE_FULL/fr_mod.log` et `fr_mod_missing.log`
(textes EN visibles et non traduits, relevés toutes les 2 s).

### Méthode

1. `override.cfg` ajoute l'autoload `FrMod="*res://MOLDRISE_FR/fr_mod.gd"`. Godot cherche dans le dossier de l'exe
   les chemins `res://` absents du `.pck`, donc le chemin relatif est portable.
2. `fr_mod.gd` :
   - **UI** : une `Translation` locale `fr`, dont les clés sont le texte EN exact. Godot traduit tout seul le `text` des Control.
   - **Dialogues / noms** : le mod modifie en mémoire les `.tres` Sprouty Dialogs mis en cache. Une réplique n'est appliquée
     que si l'EN actuel du jeu est **identique** à l'EN embarqué dans la traduction : après une MAJ, une réplique modifiée reste en EN au lieu d'afficher une traduction fausse.
   - **Textures** : `ImageTexture` + `take_over_path(chemin_original)`. Les matériaux chargés ensuite reçoivent la texture FR.
   - **Chaînes construites par le code** (`"TRADING WITH %s"`, `"3x item"`, les codes de frappe interpolés dans les dialogues…) :
     règles regex de `work/tr/patterns.json`, appliquées aux Label/Button/RichTextLabel dès que leur texte change.
3. Après une MAJ du jeu, au pire des chaînes restent en EN. **Pas de crash** : aucun asset n'est remplacé.

### Pipeline

| Étape | Commande |
|--|--|
| Extraire le projet | `tools/gdre/gdre_tools.exe --headless --recover=<MOLDRISE.pck> --output=source/recovered` |
| Inventaire EN | `python scripts/inventory.py` → `work/inventory_en.json` |
| Liste UI | `python scripts/make_ui_todo.py` → `work/tr/ui_todo.json` (ids stables) |
| Contexte d'un dialogue | `python scripts/dump_dialog.py dialog_<pnj>` (ordre de conversation) |
| Intégrer un brouillon | `python scripts/tr_merge.py work/tr/drafts/dialog_<pnj>.json` → `work/tr/dialogs/` (EN embarqué) |
| Build + QA | `python scripts/build_mod.py` (balises, placeholders, nb de lignes, EN périmé ; typo FR avec U+00A0) |
| Audit textures | `scripts/texture_sheets.py`, `scripts/glb_textures.py` → `docs/TEXTURES_VIDEOS.md` |

Règles de traduction : [`GUIDE_TRADUCTION.md`](GUIDE_TRADUCTION.md). Workflow : l'agent traduit, une IA indépendante
relit, puis Théo valide.

### Inventaire (v1.0.2, hors debug/addons)

| Type | Entrées | Mots |
|--|--|--|
| Répliques PNJ | 783 | 11 425 |
| Choix du joueur | 623 | 3 640 |
| Littéraux de scripts | 509 | 2 652 |
| Textes de scènes | 377 | 1 213 |
| Noms de persos | 34 | 68 |

### Arborescence

| Dossier | Rôle | Versionné |
|--|--|--|
| `scripts/` | inventaire, build, outils | oui |
| `mod/` | `fr_mod.gd` (runtime) | oui |
| `work/tr/` | traductions (UI, Const, dialogues, persos, patterns) | oui |
| `docs/` | guide de traduction, audit textures/vidéos | oui |
| `source/recovered` | projet récupéré par GDRE Tools v2.7.4 | **non** (contenu du jeu) |
| `tools/`, `build/`, `.venv/` | outils / sorties | non |
