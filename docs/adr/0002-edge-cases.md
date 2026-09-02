# ADR 0002 — Cas limites : décisions non spécifiées par le brief

- **Statut** : accepté
- **Date** : 2026-09-02

## Contexte

Le brief donne 5 exemples et des règles de remise, mais ne spécifie pas
certains cas que la production rencontrera.

## Décisions

| Cas | Décision | Justification |
|---|---|---|
| Panier vide | Prix **0 €**, aucune remise | Produit cartésien naturel de « rien n'est acheté » |
| Film hors saga | **Toujours 20 €**, jamais remisé | Texte du brief : « la boutique vend également d'autres films qui coûtent chacun 20 € » ; la remise porte explicitement sur « les DVDs Back to the Future achetés » |
| Doublons d'un même volet | Ne comptent **pas** comme volets distincts, mais sont **remisés** | Exemple 4 du brief : `1,2,3,2` -> 48 € = 4 × 15 × 0,8 |
| Titre inconnu / mal orthographié | Erreur 422 avec message lisible (« film inconnu ») | Un prix silencieux et faux serait pire qu'une erreur explicite ; la page web guide l'utilisateur |

## Conséquences

- Les tests d'edge cases verrouillent ces choix (`tests/test_edge_cases.py`).
- Le README documente ces règles pour le client.
