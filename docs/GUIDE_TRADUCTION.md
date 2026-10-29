# Guide de traduction MOLDRISE FR (glossaire + style)

Source de vérité pour toutes les traductions (agent, relecteur IA, Théo). ⚖️ = choix ouvert à valider par Théo.

## Univers (contexte pour traduire juste)

Horreur/humour noir. Le joueur (masculin : « dude », « bro », « a real man ») vit dans **Vista Gloria**, un immeuble
délabré, infesté de moisissure. Une mycose au pied gauche (champignon) le pousse irrésistiblement à **monter jusqu'au toit** : c'est
« the pull ». L'ascenseur est cassé, il grimpe étage par étage, rencontre des voisins, troque, rend des services.
Les riches des **étages premium** (« Top Dogs ») sont détestés. Fin : le champignon gagne. Tout le monde finit heureux sur les toits.
L'épidémie est liée aux cacahuètes KRAZY Kraunchy Nutz.

## Règles absolues (techniques)

1. **Ne jamais modifier** les balises BBCode (`[b]`, `[i]`, `[shake ...]`, `[font_size=60]`, `[quest]...[/quest]`, `[wave]`, `[color=...]`).
   Elles s'ouvrent et se ferment autour du segment FR équivalent.
2. **Ne jamais modifier** les expressions de code `{FloorEventManager.xxx()}`, `{variable}`, `%s`, `%d`, `%02d`, `%.0f%%`.
   Elles restent identiques, mais on peut les déplacer dans la phrase.
3. Les retours à la ligne `\n` sont conservés : le jeu les traite comme des « bulles » successives (`new_line_as_new_dialog`).
   Le nombre de bulles doit rester identique.
4. Longueur : rester proche de l'EN (±30 %) pour les boutons, titres et HUD. Les dialogues sont libres.
5. Typographie FR : espace insécable **U+00A0** avant `! ? : ;` et à l'intérieur des `« »`. Les polices du jeu n'ont **pas** l'espace fine U+202F ;
   `build_mod.py` convertit automatiquement U+202F en U+00A0. Toutes les autres lettres FR (é è ç œ É À « » ’ …) existent dans les polices.
   Points de suspension `…` ou `...` comme dans la source. Majuscules accentuées (É, À).

## Registre

- **Narration / système → joueur : tutoiement** (« Ton pied gauche te démange »). Cohérent avec l'esprit horreur et avec WTTG3.
- **Joueur → PNJ** : vouvoiement par défaut pour les adultes inconnus, tutoiement pour les jeunes et les marginaux (KRNL, Squatter, Dieter).
  On adapte ensuite selon la relation qui se construit.
- **PNJ → joueur** : selon le personnage (tableau ci-dessous). Pas de règle globale, mais le choix doit rester cohérent dans tout le fichier d'un personnage.
- Jurons : garder leur force (« FUCK » → « PUTAIN », « Rich assholes » → « Bande d'enfoirés de riches »). Ne pas censurer, ne pas en rajouter.
- Jeux de mots et références : les **adapter** pour qu'ils fonctionnent en FR plutôt que les traduire mot à mot. Si c'est intraduisible, le noter dans `note`.

## Personnages

| ID | Nom affiché (connu / inconnu) | FR | Voix et registre envers le joueur |
|--|--|--|--|
| old_lady | Old Lady / Old Lady | La Vieille Dame | Mamie gâteau, mielleuse et manipulatrice. **Tutoie** (« mon petit », « mon chou »). |
| brother | Miles / Man behind Door | Miles / L'homme derrière la porte | Brisé, phrases hachées. Tutoie. |
| chef | Chef Bronson / Creepy Apron Guy | Chef Bronson / Type louche en tablier | Chef excentrique et grandiloquent. Vouvoie. |
| cultist | Samuel / Weird Old Man | Samuel / Vieillard bizarre | Mystique, prêcheur. Tutoie (« mon enfant »). |
| defector | Dieter / Lanky Bloke | Dieter / Grand échalas | Familier, « dude ». Tutoie. |
| dr_lee | Dr. Lee / Asian Lady | Dr Lee / Dame asiatique | Médecin, posée. Vouvoie. |
| drinking_fountain | The most disgusting Fountain in the world / Fountain | La fontaine la plus dégueulasse du monde / Fontaine | Narration |
| ex_wife | Chaya / Tall Woman | Chaya / Grande femme | Amère. Vouvoie puis tutoie. |
| hackergirl | KRNL / Smelly Youngster | KRNL / Jeune qui pue | Ado gameuse et argot internet (« skill issue », « rizzmaxxing », « bro »). **Tutoie.** Garder l'argot gamer réellement employé en FR (« skill issue » reste tel quel). |
| janitor | Concierge / Concierge ? | Le Concierge | ⚖️ Choix actuel, à confirmer par Théo (alternative : « gardien »). Bourru, il **tutoie** le joueur ; le joueur le vouvoie. |
| lawyer | Sean the Lawyer / Creepy Suite Guy | Sean l'avocat / Type louche en costard | Jargon juridique et condescendance. Vouvoie. Références légales US (NFPA 101) conservées. |
| mediator | Meredith / Entitled looking Woman | Meredith / Femme à l'air hautain | « Karen », passive-agressive, présidente autoproclamée de la communauté. Vouvoie avec mépris. |
| nurse | Night Shift Nurse Betty / Cautious Women | Betty, infirmière de nuit / Femme méfiante | Méfiante, commerçante. Vouvoie. |
| samson | Samson / Weird Boomer | Samson / Boomer chelou | Boomer conspirationniste. Tutoie. |
| sister | Linda / Friendly Woman | Linda / Femme aimable | Douce. Vouvoie puis tutoie. |
| subletter | Squatter / Shabby Wreck | Le Squatteur / Épave miteuse | Défoncé. Tutoie. |
| vending_machine | Vending Machine | Distributeur automatique | Voix robotique |
| player | You | Toi | — |

## Glossaire

| EN | FR | Note |
|--|--|--|
| MOLDRISE | MOLDRISE | Titre, on n'y touche pas |
| Vista Gloria | Vista Gloria | Nom de l'immeuble |
| the pull | l'appel | « Trust the pull » → « Fais confiance à l'appel » |
| Top Dogs | ⚖️ les Gros Bonnets | Faction des riches. Alternatives : les Nantis, les Pontes. Apparaît aussi en graffiti. |
| The Premium Floors | Les étages de luxe | |
| The Middle Floors | Les étages intermédiaires | Titre de zone |
| Floor One / Ninth Floor | le 1er étage / le 9e étage | **On garde les numéros du jeu** (les boutons de l'ascenseur affichent ces chiffres) |
| basement | sous-sol | |
| lobby | hall d'entrée | |
| Idea / Ideas | Idée / Idées | Mécanique (touche V) |
| Infection / Hunger / Thirst | Infection / Faim / Soif | HUD |
| athlete's foot | mycose du pied | « pied d'athlète » est moins naturel en FR |
| fungus / mold / spores / mycelium | champignon / moisissure / spores / mycélium | |
| Dollar Coin | pièce d'un dollar | Monnaie du jeu. Pluriel : « pièces d'un dollar » |
| Knock | Frapper | Prompt d'interaction |
| knock pattern / code | code de frappe | |
| Infected (mode) / Story (mode) | Infecté / Histoire | |
| Deja Vu | Déjà-vu | Marqueur des réponses déjà données |
| Roca Cola, Snackers Bar, KRAZY Kraunchy Nutz, RAWBERRY ENERGY, MYKOZID 3000, Freddy Funko | inchangés | Marques fictives |
| Snackers slogan « You are not yourself when you are hungry » | « Quand t'as faim, t'es plus toi-même. » | Clin d'œil au slogan FR de Snickers |
| KRNL / Kernel | KRNL / Kernel | Pseudo de la hackeuse |
| Vlad | Vlad | |
| Our Little Family | Notre Petite Famille | Bulletin de Meredith |
| trash bag / pizza box / rusty barrel | sac poubelle / carton à pizza / baril rouillé | Conteneurs fouillables |
| Rummaging... | Fouille... | |
| THEY BUY / THEY OFFER | ACHAT / VENTE | Formulation neutre, parce que le texte est le même pour tous les marchands |
| (premium floors) gate / security gate | la grille (de sécurité) | |
| building management | la gérance | |
| fire exit / fire escape door | issue de secours | |
| the urge | la pulsion | Distinct de « the pull » = l'appel |
| foot fungus | mycose du pied | « champignon au pied » toléré dans la bouche de KRNL (argot) |
| nuts (générique) | cacahuètes | La marque reste KRAZY Kraunchy Nutz/Nuts, avec l'orthographe de la source |
| Anti-fungal lotion | lotion antifongique | |
| The Defector (surnom de Dieter chez KRNL) | le Transfuge | |
| lease / letterhead | bail / en-tête | |
| handcuffs | menottes | |
| CDC | les CDC | |
| Actions entre astérisques ou crochets | infinitif | *Regarder : X*, [Partir], [Mentir], [Donner la lettre] |
| floors in numbers | chiffres (« au 9e ») ; un **nombre** d'étages parcourus reste en lettres (« seize étages ») | |

## Format des fichiers de traduction

- `work/tr/ui.json` : `[{"en": "...", "fr": "...", "note": "..."}]`. `en` = texte EXACT tel qu'affiché à l'exécution.
- `work/tr/dialogs/<dialog_file>.json` : `{"KEY": {"en": "...", "fr": "...", "note": "..."}}`. `en` = copie exacte de l'inventaire.
- `note` est facultatif : choix discutable, jeu de mots adapté, doute de contexte.
