"""Module principal du domaine « Back to the Future ».

Ce paquet contient la logique métier pure, sans aucune dépendance
vers un framework d'interface (CLI, HTTP, web). Voir `docs/adr/0001-domain.md`.
"""

from bttf.cart import CartItem, PriceBreakdown, compute_order_total

__all__ = ["CartItem", "PriceBreakdown", "compute_order_total"]
