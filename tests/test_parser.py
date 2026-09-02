"""Tests du parseur de panier textuel.

Format d'entrée (brief) : un titre de film par ligne, dans une zone
de texte. Décisions non spécifiées documentées dans `ADR 0002`.
"""

import pytest

from bttf.parser import parse_cart, CartParsingError


def test_parse_single_title() -> None:
    # Given
    text = "Back to the Future 1"

    # When
    items = parse_cart(text)

    # Then
    assert len(items) == 1
    assert items[0].title == "Back to the Future 1"
    assert items[0].quantity == 1


def test_parse_multiple_lines_keeps_order_and_quantities() -> None:
    # Given
    text = "Back to the Future 1\nBack to the Future 2\nLa chèvre"

    # When
    items = parse_cart(text)

    # Then
    assert [i.title for i in items] == [
        "Back to the Future 1",
        "Back to the Future 2",
        "La chèvre",
    ]


def test_parse_is_case_insensitive() -> None:
    """Le magasin tolère « back to the future 1 » comme « BACK TO THE FUTURE 1 »."""
    items = parse_cart("BACK TO THE FUTURE 1")
    assert items[0].title == "Back to the Future 1"


def test_parse_trims_whitespace_and_ignores_empty_lines() -> None:
    items = parse_cart("  Back to the Future 1  \n\n   \nBack to the Future 2\n")
    assert [i.title for i in items] == ["Back to the Future 1", "Back to the Future 2"]


def test_parse_accumulates_duplicate_lines_into_quantity() -> None:
    items = parse_cart("Back to the Future 1\nBack to the Future 1")
    assert len(items) == 1
    assert items[0].quantity == 2


def test_parse_rejects_unknown_title_with_clear_message() -> None:
    with pytest.raises(CartParsingError):
        parse_cart("Back to the Future 4")


def test_parse_empty_text_returns_empty_cart() -> None:
    assert parse_cart("") == []
    assert parse_cart("\n  \n") == []
