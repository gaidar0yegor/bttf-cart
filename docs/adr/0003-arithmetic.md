# ADR 0003 — Arithmétique : entiers + Decimal pourcentage, jamais float

- **Statut** : accepté
- **Date** : 2026-09-02

## Contexte

Manipuler de l'argent en flottant binaire (`0.1 + 0.2 != 0.3`) est la
source classique de bugs de caisse. Le brief impose des remises en
pourcentage entiers (10 %, 20 %).

## Décision

- **Prix et totaux : entiers** (euros, pas de centimes dans le brief).
- **Pourcentage : entier** (`discount_percent`).
- **Arrondi du montant remisé : `Decimal` + `ROUND_HALF_UP`** (arrondi
  commercial, en faveur du client) — jamais l'arrondi bancaire par défaut
  de Python (`round(4.5) -> 4`).

## Conséquences

- Aucune erreur de représentation possible sur les sommes.
- La politique d'arrondi est un choix explicite, documenté et testé
  (`test_edge_cases.py` : 45 EUR à 10 % = 4,5 EUR -> 5 EUR).
- Si le brief évolue vers des centimes, passer à `Decimal` partout reste
  un changement localisé dans `catalog.py` et `cart.py`.
