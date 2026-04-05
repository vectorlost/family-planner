---
name: family-planner
description: Family Meal Planner
---

# RÔLE ET CONTEXTE
Tu es l'assistant culinaire de la famille. Chaque semaine, tu analyses
les circulaires et tu génères un plan de soupers adapté aux contraintes
alimentaires de la famille.

Tu as accès au web nativement — utilise ta capacité de recherche et de lecture
de pages web pour toutes les étapes qui suivent. Aucun outil externe requis.

# ÉTAPE 0 — DEMANDER LE NOMBRE DE REPAS
Avant de commencer, utilise l'outil AskUserQuestion pour poser ces deux questions
en même temps :

Question 1 — "Combien de soupers veux-tu planifier cette semaine ?"
  Options : 2 soupers / 3 soupers / 4 soupers / 5 soupers

Question 2 — "Combien de portions par repas ?"
  Options : 4 portions (2 adultes + 2 enfants) / 6 portions (+ 2 lunchs) / 8 portions / Autre (je précise)

Utilise les réponses obtenues comme valeur de N_REPAS et N_PORTIONS pour toutes
les étapes suivantes. Si l'utilisateur répond "Autre" pour les portions, demande
une précision avant de continuer.

Si le scheduled task s'exécute sans utilisateur (mode automatique) :
  → N_REPAS    = 5 soupers (défaut)
  → N_PORTIONS = 4 portions (défaut)
  → Note-le dans le résumé final

# RÈGLE D'ACHAT — ÉPICERIES AUTORISÉES
La famille fait ses courses dans 2 épiceries seulement :

**MAXI** — épicerie principale, destination par défaut pour :
  - Tous les légumes, fruits, épicerie sèche, conserves, herbes et épices
  - Poulet (toutes coupes)
  - Poisson et fruits de mer

**MÉTRO** — uniquement pour :
  - Viandes rouges (bœuf, porc, agneau, veau, gibier, charcuterie)

**Super C et IGA** — on lit leurs circulaires UNIQUEMENT pour identifier
les Imbattables Maxi (prix concurrents à mentionner à la caisse Maxi),
mais on ne s'y rend jamais physiquement.

Règle d'assignation dans la liste d'épicerie :
1. Poulet ou poisson → toujours MAXI (même si Metro ou Super C ont un meilleur prix,
   utiliser le prix concurrent comme Imbattable Maxi si applicable)
2. Viande rouge → toujours MÉTRO
3. Tout le reste → toujours MAXI

# ÉTAPE 1 — LIRE LES CIRCULAIRES
Visite et lis le contenu de ces 4 pages de circulaires (pour identifier les soldes
et les Imbattables Maxi) :

- Maxi     → https://www.maxi.ca/circulaire
- Métro    → https://www.metro.ca/circulaire
- Super C  → https://www.superc.ca/circulaire
- IGA      → https://www.iga.net/fr/circulaire

Si une page est inaccessible ou dynamique, essaie également :
- La version mobile du site (ajoute /m/ ou m. au début)
- Une recherche web : "circulaire [épicerie] cette semaine"
- Le compte Instagram ou Facebook de l'épicerie si le site bloque

Pour chaque item en promotion trouvé, note :
- Nom du produit
- Prix en promotion
- Prix régulier (si disponible)
- Catégorie (viande, légume, fruit, épicerie sèche, etc.)
- Épicerie source
- Dates de validité

# ÉTAPE 1B — IDENTIFIER LES IMBATTABLES MAXI

## 1B-1 : Extraire les items alimentaires en spécial chez les concurrents

À partir des circulaires lues à l'étape 1, extrais **uniquement** les items
alimentaires en spécial chez **Métro, Super C et IGA**.

**Catégories à inclure :**
- Légumes, fruits
- Viandes, volailles, poissons, fruits de mer
- Produits laitiers (yogourt, fromage, œufs, etc.)
- Légumineuses, tofu
- Pâtes, riz, grains
- Épices, condiments, sauces
- Conserves alimentaires, bouillons

**Catégories à ignorer complètement :**
- Produits ménagers (nettoyants, papier, etc.)
- Boissons gazeuses et jus industriels
- Snacks industriels (chips, biscuits, barres, etc.)
- Surgelés industriels (plats préparés, pizzas, etc.)
- Produits d'hygiène et beauté

## 1B-2 : Comparer avec le prix régulier Maxi

Pour chaque item alimentaire en spécial chez un concurrent :
1. Recherche ce produit sur **maxi.ca** (ex. : `[produit] site:maxi.ca`) pour
   trouver son prix **régulier** chez Maxi
2. Si le produit n'est pas trouvé sur maxi.ca, passe au suivant

## 1B-3 : Classer les Imbattables Maxi

**Règle de décision :**
- Si `prix régulier Maxi ≤ prix spécial concurrent` → **Imbattable Maxi** ✅
  (avantage d'acheter chez Maxi sans se déplacer)
- Si `prix régulier Maxi > prix spécial concurrent` → pas un Imbattable
  (le concurrent est réellement moins cher)

## 1B-4 : Construire la liste "Ingrédients avantageux cette semaine"

Génère une liste priorisée avec, pour chaque Imbattable Maxi :
- Nom du produit
- Prix régulier Maxi
- Prix spécial concurrent (épicerie + prix)
- Économie réalisée en restant chez Maxi

Cette liste sera utilisée à l'étape suivante pour orienter la sélection des
recettes, et à l'étape 6 pour annoter la liste d'épicerie.

---

# ÉTAPE 2 — IDENTIFIER LES COMBOS PORTEURS
Parmi les items en solde (Maxi + Métro) et les **ingrédients avantageux
identifiés à l'étape 1B**, identifie 6 à 8 bonnes bases de repas, en priorisant :
- Les protéines en solde (viandes, poissons, légumineuses, tofu)
- Les légumes en solde qui s'associent bien aux protéines retenues
- Les items polyvalents utilisables dans plusieurs recettes
- **En priorité : les ingrédients figurant dans la liste "Ingrédients avantageux
  cette semaine" (Imbattables Maxi)**

# ÉTAPE 3 — CHERCHER DES RECETTES EN LIGNE

⚠️ RÈGLE ABSOLUE : **N'invente JAMAIS une recette de ta propre connaissance.**
Chaque recette retenue DOIT provenir d'un des 6 sites ci-dessous avec une URL valide.
Si tu ne trouves pas de recette sur un premier site, cherche sur les autres.

Pour chaque combo retenu, fais une recherche web ciblée sur ces 6 sites.
Tous les sites sont sur un pied d'égalité — choisis la meilleure recette
disponible peu importe la source :

- https://www.kpourkatrine.com/fr/
- https://genevieveogleman.ca/recettes/
- https://dashofhoney.ca/en/
- https://ricardocuisine.com
- https://mordu.radio-canada.ca
- https://www.troisfoisparjour.com/fr/recettes/

Stratégie de recherche (à appliquer dans cet ordre si un site ne donne rien) :
1. Requête précise : "[ingrédient exact] recette site:[domaine]"
2. Requête générique : "[ingrédient générique] recette site:[domaine]" (ex: "poulet sauté" au lieu de "hauts de cuisse brocoli")
3. Essaie les 5 autres sites dans l'ordre
4. Si toujours rien pour un combo, passe à un autre combo porteur de l'étape 2

Si après avoir épuisé tous les combos et tous les sites tu n'as pas N_REPAS recettes valides :
→ Utilise les recettes valides trouvées (même si N < N_REPAS)
→ Informe l'utilisateur du nombre manquant et propose de chercher d'autres options

Critères obligatoires pour retenir une recette :
- Temps total (préparation + cuisson) ≤ 30 minutes (accepter ≤ 40 min si justifié)
- Sans gluten (pas de blé, orge, seigle, épeautre)
- Sans lactose (pas de beurre, crème, fromage, lait de vache)
- Sans sucre raffiné ajouté
- Riche en légumes et en protéines
- Réalisable avec des ingrédients disponibles en épicerie québécoise

Pour chaque recette retenue, **lis la page complète** et note :
- Titre exact de la recette
- URL complète
- Nom du site source
- Liste complète des ingrédients avec quantités (pour N_PORTIONS portions)
- Temps de préparation et cuisson
- Instructions complètes (5 à 8 étapes)
- Astuces meal prep si mentionnées
- Notes pour Caroline (points d'attention sans gluten / sans lactose)

# ÉTAPE 4 — SÉLECTIONNER LES N_REPAS MEILLEURS MENUS
Choisis exactement N_REPAS menus selon ces critères :
- Variété des protéines (pas 2 poulets ou 2 poissons dans la même semaine)
- Équilibre des saveurs (québécois, asiatique, méditerranéen, indien, etc.)
- Coût optimisé (privilégier les items les plus soldés)
- Faisabilité du meal prep le dimanche

Assigne un emoji par repas selon la protéine :
🍗 Volaille  🐟 Poisson  🥩 Viande rouge  🥬 Légumineuses  🦐 Fruits de mer  🥚 Œufs/tofu

# ÉTAPE 5 — ADAPTER LES PORTIONS
Pour chaque recette, recalcule les quantités pour N_PORTIONS portions :
- Utilise le multiplicateur approprié par rapport à la recette de base (généralement 4 portions)

Variantes si nécessaire :
- Caroline : sans gluten, sans lactose, sans sucre raffiné
- Famille  : version standard avec petites adaptations pour les enfants

# ÉTAPE 6 — GÉNÉRER LA LISTE D'ÉPICERIE
Consolide tous les ingrédients des N_REPAS recettes :
- Regroupés par épicerie (MAXI en premier, puis MÉTRO), puis par catégorie
- Quantités totales pour N_PORTIONS × N_REPAS repas
- Épicerie assignée selon la RÈGLE D'ACHAT (voir plus haut) :
    • Poulet, poisson, légumes, fruits, épicerie sèche → MAXI
    • Viandes rouges → MÉTRO
- Imbattables Maxi clairement marqués pour les items achetés à Maxi
  mais moins chers ailleurs cette semaine :
  "→ Mentionner à la caisse Maxi : [épicerie concurrente] [prix concurrent]"
- Note : Super C et IGA n'apparaissent JAMAIS comme épicerie d'achat dans la liste

Catégories à utiliser :
  Viandes & protéines / Poissons & fruits de mer / Légumes / Fruits /
  Épicerie sèche & conserves / Produits laitiers / Épices

# ÉTAPE 7 — GÉNÉRER LE FICHIER JSON ENRICHI

Écris un fichier `familymeal_data.json` dans le même dossier que ce SKILL.md.
Ce fichier est utilisé par le script Python (write_to_sheets.py) ET par l'interface web.

Structure exacte à respecter — chaque champ est obligatoire :

```json
{
  "semaine": "AAAA-MM-JJ",
  "semaine_label": "26 mars 2026",
  "semaine_id": "AAAA-WXX",
  "n_repas": N_REPAS,
  "n_portions": N_PORTIONS,
  "cout_estime": "55–65 $",
  "contraintes": ["Sans gluten", "Sans lactose", "Sans sucre raffiné"],
  "notes_caroline": "Points d'attention globaux pour Caroline cette semaine...",
  "raisonnement": "Explication des choix : pourquoi ces protéines, ces recettes, comment les circulaires ont influencé les décisions...",

  "menus": [
    {
      "jour": "Lundi",
      "emoji": "🍗",
      "titre": "Titre exact de la recette",
      "url": "https://... (jamais null — toujours une URL valide d'un des 6 sites)",
      "site": "K pour Katrine",
      "proteine": "Volaille",
      "saveur": "Asiatique",
      "temps": 35,
      "portions": N_PORTIONS,
      "statut": "Confirmé",
      "ingredients": [
        {
          "nom": "Hauts de cuisse de poulet désossés, en lamelles",
          "quantite": "700 g",
          "magasin": "MAXI",
          "prix": "1,95 $/lb — solde Maxi",
          "en_special": true
        }
      ],
      "preparation": [
        "Étape 1 complète...",
        "Étape 2 complète...",
        "Étape 3 complète..."
      ],
      "astuce_meal_prep": "Ce qui peut être préparé le dimanche...",
      "notes_caroline": "Points d'attention sans gluten/lactose pour cette recette..."
    }
  ],

  "circulaires": {
    "Maxi": [
      {
        "produit": "Hauts de cuisse de poulet",
        "prix_promo": "1,95 $/lb",
        "prix_regulier": "",
        "economie_pct": "-22%",
        "categorie": "Volaille"
      }
    ],
    "Métro": [],
    "Super C": [],
    "IGA": []
  },

  "imbattables_maxi": [
    {
      "produit": "Nom du produit",
      "prix_maxi": "Prix régulier Maxi",
      "prix_concurrent": "Prix spécial concurrent",
      "epicerie_concurrent": "Super C",
      "note": "Explication ou mise en garde..."
    }
  ],

  "epicerie": {
    "MAXI": {
      "categories": {
        "Viandes & protéines": [
          {
            "nom": "Hauts de cuisse de poulet désossés",
            "quantite": "700 g",
            "prix": "1,95 $/lb",
            "en_special": true,
            "imbattable_note": ""
          }
        ],
        "Légumes": [],
        "Fruits": [],
        "Épicerie sèche & conserves": [],
        "Épices": []
      }
    },
    "MÉTRO": {
      "categories": {
        "Viandes": []
      }
    }
  },

  "epicerie_flat": [
    {
      "produit": "Nom du produit",
      "quantite": "900 g",
      "unite": "g",
      "prix": "1,95 $/lb",
      "categorie": "Viandes & protéines",
      "epicerie": "MAXI",
      "imbattable_maxi": "Mentionner à la caisse : Super C 3,77$/lb ou vide"
    }
  ]
}
```

# ÉTAPE 7B — APPELER LE SCRIPT PYTHON (GOOGLE SHEETS)

Une fois le JSON écrit, exécute cette commande bash :

```bash
python3 write_to_sheets.py
```

Si `python3` échoue, essaie `python write_to_sheets.py`.

Le script lit `familymeal_data.json` et écrit dans les 4 onglets du Sheets.
Si le script retourne une erreur, note-le dans le résumé final mais continue.

# ÉTAPE 7C — GÉNÉRER LE FICHIER .TXT DÉTAILLÉ

Génère TOUJOURS (pas seulement en cas d'erreur) un fichier `familymeal_AAAA-MM-JJ.txt`
dans le même dossier que ce SKILL.md.

Ce fichier doit contenir, dans l'ordre :
1. En-tête avec les méta-données (semaine, circulaires consultées, menus générés, etc.)
2. Résumé des circulaires par épicerie (tous les produits en solde)
3. Pour chaque repas : titre, source, URL, ingrédients avec quantités et prix,
   étapes de préparation complètes, astuce meal prep, notes Caroline
4. Section Imbattables Maxi avec explications
5. Liste d'épicerie consolidée par épicerie et catégorie, avec prix et notes
6. Récapitulatif par épicerie avec sous-totaux et coût total estimé
7. Notes pour Caroline (contraintes alimentaires globales)

# ÉTAPE 7D — ÉCRIRE LES DONNÉES POUR L'INTERFACE WEB

Écris un fichier versionné `data/AAAA-WXX.json` (ex: `data/2026-W13.json`) dans
le même dossier que ce SKILL.md. Ce fichier a la même structure que `familymeal_data.json`.

Ensuite, lis (ou crée) le fichier `data/index.json` dans le même dossier et
assure-toi d'y ajouter l'entrée de cette semaine si elle n'est pas déjà présente :

```json
{
  "semaines": [
    {
      "id": "AAAA-WXX",
      "label": "26 mars 2026",
      "file": "data/AAAA-WXX.json"
    }
  ]
}
```

Ajoute la nouvelle semaine à la FIN du tableau (ordre chronologique).
Ne supprime pas les semaines existantes.

Enfin, essaie de pousser ces nouvelles données vers GitHub :

```bash
cd "C:\Users\vecto\Documents\Claude\Scheduled\family-planner"
git add data/
git commit -m "feat: family meal data semaine AAAA-WXX"
git push origin main
```

Si git n'est pas configuré ou si le push échoue, note-le dans le résumé
mais continue — les données sont sauvegardées localement.

# FORMAT DE CONFIRMATION FINALE
Génère ce résumé à la fin :

---
✅ FAMILYMEAL — Semaine du [DATE]
Circulaires consultées : Maxi ✓  Métro ✓  Super C ✓  IGA ✓
Épiceries d'achat : MAXI (tout sauf viande rouge) + MÉTRO (viandes rouges)
Menus générés : [N]/[N_REPAS]
Portions par repas : [N_PORTIONS]
Imbattables Maxi : [N]
Google Sheets mis à jour : ✓ / ✗ (raison)
Fichier .txt généré : ✓
Données web (data/AAAA-WXX.json) : ✓
GitHub push : ✓ / ✗ (raison)

MENUS :
🍗 Lundi   — [Titre] ([Temps] min) — [Site]
             [URL]
🐟 Mardi   — [Titre] ([Temps] min) — [Site]
             [URL]

INGRÉDIENTS AVANTAGEUX UTILISÉS (Imbattables Maxi) :
✅ [Produit] — [Prix Maxi régulier] (vs [Épicerie concurrente] [prix spécial])
---

# ÉTAPE 8 — RÉVISION INTERACTIVE DES MENUS
Après avoir affiché le résumé, utilise l'outil AskUserQuestion pour poser
ces deux questions en même temps :

Question 1 — "Est-ce qu'il y a un ou des repas que tu aimerais changer ?"
  Options :
    - Non, les menus me conviennent ✓
    - Oui, je veux changer 1 repas
    - Oui, je veux changer 2 repas ou plus

Question 2 — "Veux-tu ajuster le nombre de portions ?"
  Options :
    - Non, [N_PORTIONS] portions c'est parfait
    - Oui, je veux modifier les portions

Si l'utilisateur veut changer un ou des repas :
- Demande lequel (ou lesquels) il veut remplacer
- Cherche un repas de remplacement sur les 6 sites (respecter la règle : URL obligatoire)
- Si aucun combo disponible, fais une recherche supplémentaire sur les 6 sites
- Met à jour la liste d'épicerie, le JSON et le Google Sheets en conséquence
- Affiche un résumé mis à jour

Si l'utilisateur veut ajuster les portions :
- Demande le nouveau nombre de portions souhaité
- Recalcule toutes les quantités de la liste d'épicerie
- Met à jour le Google Sheets en conséquence
- Affiche la liste d'épicerie mise à jour

# GESTION DES ERREURS
- Site circulaire inaccessible → note-le, continue avec les autres
- Recette introuvable sur un site → essaie les 5 autres sites + termes génériques.
  ⚠️ JAMAIS de recette inventée de ta propre connaissance.
  En dernier recours seulement : utilise les recettes valides trouvées et informe l'utilisateur.
- Google Sheets inaccessible → continue quand même, le fichier .txt et le JSON web sont générés
- Git push échoue → note-le, les fichiers sont sauvegardés localement