"""Tests « golden » : les 5 exemples fournis dans l'énoncé d'Ekinox.

Chaque exemple du brief devient un test paramétré : la spécification
est mécanisée telle quelle, et toute régression de prix est détectée.
"""

import pytest

from bttf.cart import compute_order_total, CartItem

# Chaque cas : (items, prix_attendu)
GOLDEN_CASES: list[tuple[list[CartItem], int]] = [
    # Exemple 1 : 3 volets différents -> -20 %
    (
        [
            CartItem(title="Back to the Future 1", quantity=1),
            CartItem(title="Back to the Future 2", quantity=1),
            CartItem(title="Back to the Future 3", quantity=1),
        ],
        36,
    ),
    # Exemple 2 : 2 volets différents -> -10 %
    (
        [
            CartItem(title="Back to the Future 1", quantity=1),
            CartItem(title="Back to the Future 3", quantity=1),
        ],
        27,
    ),
    # Exemple 3 : 1 volet seul -> pas de remise
    (
        [
            CartItem(title="Back to the Future 1", quantity=1),
        ],
        15,
    ),
    # Exemple 4 : 3 volets + doublon -> -20 % sur les 4 DVD
    (
        [
            CartItem(title="Back to the Future 1", quantity=1),
            CartItem(title="Back to the Future 2", quantity=1),
            CartItem(title="Back to the Future 3", quantity=1),
            CartItem(title="Back to the Future 2", quantity=1),
        ],
        48,
    ),
    # Exemple 5 : saga complète + film hors saga -> remise sur la saga uniquement
    (
        [
            CartItem(title="Back to the Future 1", quantity=1),
            CartItem(title="Back to the Future 2", quantity=1),
            CartItem(title="Back to the Future 3", quantity=1),
            CartItem(title="La chèvre", quantity=1),
        ],
        56,
    ),
]


@pytest.mark.parametrize("items,expected", GOLDEN_CASES, ids=[f"exemple_{i}" for i in range(1, 6)])
def test_golden_cases_from_the_brief(items: list[CartItem], expected: int) -> None:
    """Chaque exemple de l'énoncé doit produire exactement le prix annoncé."""
    # Given / When
    total = compute_order_total(items)

    # Then
    assert total == expected
