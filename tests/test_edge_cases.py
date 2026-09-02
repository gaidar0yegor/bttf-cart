"""Cas limites : les exemples du brief ne couvrent pas tout.

Ces tests verrouillent le comportement attendu sur les cas qui
« cassent en production » : panier vide, doublons, films hors saga,
sans spécification explicite dans l'énoncé (décisions documentées
dans `docs/adr/0002-edge-cases.md`).
"""


from bttf.cart import CartItem, compute_order_total, compute_price_breakdown
from bttf.catalog import SAGA_TITLES

SAGA_1, SAGA_2, SAGA_3 = sorted(SAGA_TITLES)


def test_empty_cart_costs_zero() -> None:
    """Un panier vide coûte 0 € (aucune ligne, aucune remise)."""
    assert compute_order_total([]) == 0


def test_single_non_saga_movie_costs_20() -> None:
    """Un film hors saga seul ne bénéficie d'aucune remise."""
    assert compute_order_total([CartItem(title="La chèvre", quantity=1)]) == 20


def test_duplicates_do_not_count_as_distinct() -> None:
    """Deux exemplaires du même volet ne déclenchent pas la remise « 2 volets »."""
    items = [CartItem(title=SAGA_1, quantity=2)]
    assert compute_order_total(items) == 30


def test_duplicates_do_not_raise_the_discount() -> None:
    """Ajouter un doublon ne change pas le palier de remise (exemple 4 du brief)."""
    two_distinct_then_duplicate = [
        CartItem(title=SAGA_1),
        CartItem(title=SAGA_2),
        CartItem(title=SAGA_2),  # doublon
    ]
    two_distinct_only = [
        CartItem(title=SAGA_1),
        CartItem(title=SAGA_2),
    ]
    assert compute_order_total(two_distinct_then_duplicate) == 40
    assert compute_order_total(two_distinct_only) == 27


def test_multiple_quantities_inside_one_item() -> None:
    """quantity=2 équivaut à deux lignes de quantity=1 (invariant d'arithmétique)."""
    as_one_line = [CartItem(title=SAGA_1, quantity=2)]
    as_two_lines = [CartItem(title=SAGA_1), CartItem(title=SAGA_1)]
    assert compute_order_total(as_one_line) == compute_order_total(as_two_lines)


def test_non_saga_movies_are_never_discounted() -> None:
    """La remise ne s'applique qu'aux DVD de la saga, jamais aux autres films."""
    items = [
        CartItem(title=SAGA_1),
        CartItem(title=SAGA_2),
        CartItem(title=SAGA_3),
        CartItem(title="La chèvre", quantity=2),
    ]
    breakdown = compute_price_breakdown(items)
    assert breakdown.discount_percent == 20
    assert breakdown.other_line_total == 40  # 2 x 20 EUR, non remisés
    assert breakdown.total == 36 + 40  # saga remisée + films hors saga


def test_breakdown_is_consistent() -> None:
    """total = subtotal - discount, et subtotal = saga + autres."""
    items = [
        CartItem(title=SAGA_1),
        CartItem(title=SAGA_2),
        CartItem(title="La chèvre"),
    ]
    breakdown = compute_price_breakdown(items)
    assert breakdown.subtotal == breakdown.saga_line_total + breakdown.other_line_total
    assert breakdown.total == breakdown.subtotal - breakdown.discount_amount


def test_discount_amount_is_the_documented_percentage() -> None:
    """10 % de 30 = 3 ; 20 % de 45 = 9 (exemples 2 et 5)."""
    two = compute_price_breakdown([CartItem(title=SAGA_1), CartItem(title=SAGA_3)])
    assert two.discount_percent == 10
    assert two.discount_amount == 3

    three = compute_price_breakdown(
        [CartItem(title=SAGA_1), CartItem(title=SAGA_2), CartItem(title=SAGA_3)]
    )
    assert three.discount_percent == 20
    assert three.discount_amount == 9
