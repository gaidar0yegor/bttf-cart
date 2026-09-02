"""Panier et calcul du prix de commande.

Le calcul reste en arithmétique entière (prix et quantités sont des
entiers, les remises sont des pourcentages entiers) : pas de flottant
pour manipuler de l'argent, et donc aucune erreur d'arrondi possible.

Règles du brief :
- 2 volets différents -> remise de 10 % sur tous les DVD de la saga ;
- 3 volets différents -> remise de 20 % sur tous les DVD de la saga ;
- les films hors saga ne sont jamais remisés.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from bttf.catalog import is_saga_movie, get_price

# Remises exprimées en pourcentage entier (10 % -> 90 % du prix).
DISCOUNT_PCT_2_DISTINCT: int = 10
DISCOUNT_PCT_3_DISTINCT: int = 20


@dataclass(frozen=True)
class CartItem:
    """Une ligne de panier : un titre et une quantité."""

    title: str
    quantity: int = 1


@dataclass(frozen=True)
class PriceBreakdown:
    """Détail du calcul : sous-total, remise, total.

    Exposé tel quel par l'API et l'interface web : le client voit
    comment le prix est obtenu, sans magie.
    """

    subtotal: int
    saga_line_total: int
    other_line_total: int
    discount_percent: int
    discount_amount: int
    total: int


def _discount_percent(distinct_saga_titles: int) -> int:
    """Pourcentage de remise selon le nombre de volets différents."""
    if distinct_saga_titles >= 3:
        return DISCOUNT_PCT_3_DISTINCT
    if distinct_saga_titles == 2:
        return DISCOUNT_PCT_2_DISTINCT
    return 0


def compute_order_total(items: list[CartItem]) -> int:
    """Prix total de la commande, toutes remises appliquées."""
    return compute_price_breakdown(items).total


def compute_price_breakdown(items: list[CartItem]) -> PriceBreakdown:
    """Calcule le détail complet de la commande (sous-total, remise, total).

    La remise s'applique à *tous* les DVD de la saga présents dans le
    panier (y compris les doublons), dès lors que le panier contient
    2 ou 3 volets *différents* (cf. brief, exemple 4).
    """
    distinct_saga_titles: set[str] = set()
    saga_line_total = 0
    other_line_total = 0

    for item in items:
        line_total = get_price(item.title) * item.quantity
        if is_saga_movie(item.title):
            distinct_saga_titles.add(item.title)
            saga_line_total += line_total
        else:
            other_line_total += line_total

    discount_percent = _discount_percent(len(distinct_saga_titles))
    subtotal = saga_line_total + other_line_total
    discount_amount = _percent_of(discount_percent, saga_line_total)

    return PriceBreakdown(
        subtotal=subtotal,
        saga_line_total=saga_line_total,
        other_line_total=other_line_total,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        total=subtotal - discount_amount,
    )


def _percent_of(percent: int, amount: int) -> int:
    """percent % de amount, arrondi à l'unité.

    La politique d'arrondi est explicite : ROUND_HALF_UP (arrondi
    commercial, en faveur du client), jamais l'arrondi bancaire
    par défaut de Python. Documenté dans `docs/adr/0003-arithmetic.md`.
    """
    if percent == 0 or amount == 0:
        return 0
    ratio = Decimal(percent) / Decimal(100)
    return int((Decimal(amount) * ratio).to_integral_value(rounding=ROUND_HALF_UP))
