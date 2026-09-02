# BTTF Cart

Calculeur de panier DVD — exercice technique Ekinox.

Une **Web App** qui lit un panier saisi sous forme de texte (un film par
ligne) et renvoie le **prix de la commande**, avec le détail du calcul.
La remise « Back to the Future » est appliquée automatiquement.

## Règles métier

| Article | Prix |
|---|---|
| DVD « Back to the Future 1 / 2 / 3 » | 15 € |
| Tout autre film (ex. « La chèvre ») | 20 € |

| Achat | Remise |
|---|---|
| 2 volets **différents** de la saga | −10 % sur tous les DVD de la saga |
| 3 volets **différents** de la saga | −20 % sur tous les DVD de la saga |

- La remise s'applique à **tous** les DVD de la saga du panier (doublons
  compris) dès lors que le panier contient 2 ou 3 volets différents.
- Les films hors saga ne sont **jamais** remisés.
- Panier vide → 0 €. Titre inconnu → erreur explicite (422), jamais de
  prix silencieux et faux.

Exemples du brief (mécanisés dans `tests/test_golden_cases.py`) :

| Entrée | Sortie |
|---|---|
| 1, 2, 3 | 36 |
| 1, 3 | 27 |
| 1 | 15 |
| 1, 2, 3, 2 | 48 |
| 1, 2, 3, La chèvre | 56 |

## Démarrage rapide

Prérequis : Python ≥ 3.11 et [Poetry](https://python-poetry.org/).

```bash
make install        # poetry install --with dev
make test           # pytest + couverture (>= 95 %)
```

### API web (interface du brief)

```bash
make run-api        # http://localhost:8000
```

Ouvrez http://localhost:8000 : saisissez un panier (un film par ligne),
cliquez « Calculer le prix ». La documentation OpenAPI est sur
http://localhost:8000/docs.

```bash
curl -s http://localhost:8000/api/price \
  -H 'Content-Type: application/json' \
  -d '{"cart_text": "Back to the Future 1\nBack to the Future 2\nBack to the Future 3"}'
# -> {"total":36,"breakdown":{...}}
```

### CLI

```bash
echo "Back to the Future 1
Back to the Future 2" | make run-cli
# -> 27
```

## Architecture

```
src/bttf/
├── catalog.py   # prix et appartenance à la saga (seule source de vérité)
├── cart.py      # calcul du panier : sous-total, remise, total
├── parser.py    # texte -> lignes de panier (casse insensible, doublons agrégés)
├── api.py       # adaptateur FastAPI (OpenAPI sur /docs)
├── cli.py       # adaptateur ligne de commande
└── static/      # page web unique (vanilla HTML/CSS/JS)
```

Le **noyau de domaine** (`catalog.py`, `cart.py`, `parser.py`) est pur :
aucune dépendance vers un framework. Les adaptateurs (API, CLI, web)
sont de minces couches autour de lui. Voir les **ADR** dans
`docs/adr/` pour la justification de chaque décision.

## Qualité

- **TDD** : les 5 exemples du brief sont les tests « golden » du projet
  (`tests/test_golden_cases.py`) — la spécification est mécanisée.
- **Cas limites** verrouillés (`tests/test_edge_cases.py`), y compris un
  bogue d'arrondi réel détecté par les propriétés (`round(4.5) -> 4`).
- **Propriétés** (Hypothesis) : invariants vérifiés sur des milliers de
  paniers générés (`tests/test_properties.py`).
- **Lint** : `ruff` · **Types** : `mypy --strict` · **Couverture** ≥ 95 %.
- **CI** : GitHub Actions (lint + types + tests) sur chaque push/PR.

## Décisions documentées

- `docs/adr/0001-domain.md` — noyau pur, adaptateurs ; pourquoi pas
  d'architecture « ports & adapters » formelle.
- `docs/adr/0002-edge-cases.md` — panier vide, doublons, films inconnus.
- `docs/adr/0003-arithmetic.md` — entiers + `Decimal` `ROUND_HALF_UP`,
  jamais de flottant pour l'argent.
