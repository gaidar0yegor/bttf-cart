"""Tests par propriétés (Hypothesis).

Des invariants structurels, générés sur des milliers de paniers
aléatoires : ce que des exemples choisis à la main ne peuvent pas
prouver. L'argent est de l'arithmétique : on vérifie des égalités,
pas des seuils flous.
"""

from bttf.cart import CartItem, compute_order_total, compute_price_breakdown
from bttf.catalog import OTHER_MOVIE_PRICE, SAGA_PRICE, SAGA_TITLES
from hypothesis import given, settings
from hypothesis import strategies as st

cart_strategy = st.lists(
    st.builds(
        CartItem,
        title=st.one_of(st.sampled_from(sorted(SAGA_TITLES)), st.text(min_size=1)),
        quantity=st.integers(min_value=1, max_value=10),
    ),
    max_size=20,
)


@given(cart_strategy)
@settings(max_examples=500)
def test_total_never_exceeds_naive_sum(items: list[CartItem]) -> None:
    """La remise ne peut que réduire le prix : jamais le contraire."""
    naive_sum = sum(
        (SAGA_PRICE if title in SAGA_TITLES else OTHER_MOVIE_PRICE) * quantity
        for title, quantity in ((i.title, i.quantity) for i in items)
    )
    assert compute_order_total(items) <= naive_sum


@given(cart_strategy)
@settings(max_examples=500)
def test_discount_is_an_integer_percentage_of_saga_line(
    items: list[CartItem],
) -> None:
    """Le montant remisé est exactement (pourcentage entier) x (ligne saga)."""
    breakdown = compute_price_breakdown(items)
    expected = breakdown.saga_line_total * breakdown.discount_percent // 100
    # round() bancaire : on tolère l'écart d'arrondi à 1 unité maximum.
    assert abs(breakdown.discount_amount - expected) <= 1


@given(cart_strategy)
@settings(max_examples=500)
def test_non_saga_items_never_discounted(items: list[CartItem]) -> None:
    """Seuls les DVD de la saga contribuent au montant remisé."""
    breakdown = compute_price_breakdown(items)
    if breakdown.discount_percent == 0:
        assert breakdown.discount_amount == 0
    else:
        assert breakdown.discount_amount <= breakdown.saga_line_total


@given(cart_strategy)
@settings(max_examples=500)
def test_breakdown_arithmetic_is_consistent(items: list[CartItem]) -> None:
    """Invariant comptable : total + remise = sous-total = saga + autres."""
    b = compute_price_breakdown(items)
    assert b.subtotal == b.saga_line_total + b.other_line_total
    assert b.total == b.subtotal - b.discount_amount
    assert b.discount_percent in (0, 10, 20)


@given(cart_strategy)
@settings(max_examples=500)
def test_adding_a_duplicate_never_changes_the_discount_tier(
    items: list[CartItem],
) -> None:
    """Doubler un article ne change jamais le palier de remise."""
    if not items:
        return
    duplicated = items + [items[0]]
    before = compute_price_breakdown(items)
    after = compute_price_breakdown(duplicated)
    assert after.discount_percent == before.discount_percent
