# ADR 0001 — Architecture : noyau de domaine pur, interfaces adaptatrices

- **Statut** : accepté
- **Date** : 2026-09-02

## Contexte

L'exercice demande une « Web App » capable de lire un panier textuel et de
renvoyer un prix, « comme si elle était réalisée pour un client » et en
« posant les bonnes bases de travail de votre future équipe ».

## Décision

Le calcul du prix est un **noyau de domaine pur** (`src/bttf/`) sans aucune
dépendance vers un framework d'interface (HTTP, CLI, web). Les interfaces
(`cli.py`, `api.py`, page web) sont de minces adaptateurs autour de ce noyau.

## Conséquences

- La logique métier est testable sans serveur, sans HTTP, sans navigateur.
- Ajouter un quatrième point d'entrée (file d'attente, batch, agent LLM) ne
  touche pas le domaine.
- La règle « chaque décision se défend en une phrase » est respectée : la
  phrase est « le prix ne doit pas dépendre du chemin par lequel le panier
  arrive ».

## Alternatives écartées

- **Logique dans un script unique** : infalsifiable, non réutilisable,
  n'établit aucune base pour une équipe.
- **Hexagonal Architecture formelle (ports protocoles abstraits)** : la
  cérémonie (classes d'interfaces pour 3 adaptateurs) n'apporte rien en
  Python, où l'interface est implicite.
- **Persistance / file de messages / microservices** : l'état d'une
  commande est un panier : une requête. Aucune persistance exigée par le
  brief.
