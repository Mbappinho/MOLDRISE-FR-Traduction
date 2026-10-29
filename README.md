# MOLDRISE — Traduction française <a href='https://ko-fi.com/T1P023QR7T' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

Traduction française **non officielle** et gratuite de [*MOLDRISE*](https://store.steampowered.com/app/4519130/), faite par un fan.

Elle couvre l'interface, les objets, tous les dialogues, les noms des personnages, les succès et la nouvelle fin.

> **Tu veux juste jouer en français ?** Va directement à [Installation](#installation).

---

## Ce qui est traduit

| | |
|--|--|
| Dialogues | Les 20 personnages, y compris le Dr Robinson de la fin médicale |
| Interface | Menus, paramètres, inventaire, boutique, écrans de mort, tutoriels |
| Objets | Noms et descriptions |
| Pensées du personnage | Monologues, voix du champignon, hallucinations |
| Succès | Noms et descriptions, avec les jeux de mots adaptés en français |
| Non traduit | Le texte dessiné dans le décor (panneaux, graffitis) et dans les vidéos |

Au total, **2 257 textes** sont traduits, soit environ 20 000 mots. Chaque personnage garde sa propre voix, avec un tutoiement ou un vouvoiement choisi selon son caractère. Les jeux de mots ont été adaptés plutôt que traduits mot à mot.

## Compatibilité

| | |
|--|--|
| Version du jeu | **Steam, version 1.2.x** (build `25670818`) |
| Système | Windows |
| Fichiers du jeu modifiés | **Aucun** |

La traduction utilise le **système de langues officiel** du jeu. Elle ne touche à aucun fichier de MOLDRISE et ne peut pas le faire planter.

Après une mise à jour du jeu, les textes ajoutés ou modifiés par le développeur s'afficheront simplement en anglais, le temps qu'une nouvelle version de la traduction sorte.

## Installation

1. Télécharge `MOLDRISE-FR.zip` dans les [Releases](../../releases).
2. Ouvre l'explorateur Windows, colle ceci dans la barre d'adresse, puis appuie sur Entrée :
   ```
   %APPDATA%\Raffa\MOLDRISE_FULL
   ```
3. Si aucun dossier `translations` n'existe à cet endroit, crée-le.
4. Dézippe l'archive dans `translations`. Tu dois obtenir :
   ```
   MOLDRISE_FULL\translations\fr\pack.cfg
   MOLDRISE_FULL\translations\fr\dialog_....csv
   ...
   ```
5. Lance le jeu, puis choisis **Settings → Language → Français**.

> Le dossier `MOLDRISE_FULL` n'existe pas ? Lance le jeu une fois, puis quitte-le : il sera créé.

### Mettre à jour

Supprime l'ancien dossier `translations\fr`, puis refais l'étape 4 avec la nouvelle version.

### Désinstaller

Supprime le dossier `%APPDATA%\Raffa\MOLDRISE_FULL\translations\fr`. Le jeu repasse en anglais.

## Un souci ?

Si tu repères un texte encore en anglais, une faute ou un texte qui déborde de son cadre, ouvre une [issue](../../issues). Joins-y **une capture d'écran** et l'endroit du jeu où tu l'as vu. Une réplique se corrige en quelques secondes.

## Soutenir le projet

La traduction est et restera gratuite. Si elle t'a plu, tu peux m'offrir un café :

<a href='https://ko-fi.com/T1P023QR7T' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

Et surtout, **soutiens le développeur**. Achète le jeu, laisse-lui une évaluation sur Steam, et passe sur son [Discord](https://discord.raffaelepicca.com).

## Crédits

- **Jeu :** *MOLDRISE*, par Raffaele Picca. Tous droits réservés à leur auteur.
- **Traduction française :** Mbappinho ([Ko-fi](https://ko-fi.com/T1P023QR7T)).
- Autre traduction : [Welcome to the Game III en français](https://github.com/Mbappinho/WTTG3-FR-Traduction).

## Pour les contributeurs

La partie technique se trouve dans `docs/` :

- [`GUIDE_TRADUCTION.md`](docs/GUIDE_TRADUCTION.md) : règles de traduction, registre de chaque personnage, glossaire. À lire avant toute correction.
- [`DEVELOPPEMENT.md`](docs/DEVELOPPEMENT.md) : comment le pack est construit, comment le mettre à jour après un patch du jeu, et l'historique du projet.

Le pack prêt à l'emploi se trouve dans [`translations/fr/`](translations/fr) (clés officielles du jeu → français). Pour proposer une correction, ouvre une issue ou une PR sur la ligne concernée du CSV. Les fichiers de travail, qui contiennent le texte anglais du jeu, ne sont pas publiés.

## Avertissement

Projet de fan, non affilié au développeur de MOLDRISE et non approuvé par lui. *MOLDRISE* et ses contenus appartiennent à leur auteur. Ce dépôt ne contient aucun fichier du jeu.
