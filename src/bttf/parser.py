"""Parseur de panier textuel.

Le format d'entrée est celui du brief : un titre de film par ligne.
Le parseur tolère la casse et les espaces, accumule les doublons en
quantité, et rejette les titres inconnus avec un message explicite.
"""

from bttf.cart import CartItem
from bttf.catalog import SAGA_TITLES

# Titres « connus » : les titres d'acteurs inconnus sont refusés
# explicitement (ADR 0002) — un prix faux vaut moins que pas de prix.
KNOWN_TITLES: frozenset[str] = SAGA_TITLES | frozenset({"La chèvre"})

# Correspondance insensible à la casse : titre canonique -> titre du catalogue.
_CANONICAL_TITLES: dict[str, str] = {t.casefold(): t for t in KNOWN_TITLES}


class CartParsingError(ValueError):
    """Le texte saisi ne correspond pas à un panier valide."""


def parse_cart(text: str) -> list[CartItem]:
    """Convertit le texte saisi en lignes de panier.

    Raises:
        CartParsingError: si une ligne référence un film inconnu.
    """
    items_by_title: dict[str, int] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        canonical_title = _CANONICAL_TITLES.get(line.casefold())
        if canonical_title is None:
            raise CartParsingError(f"Film inconnu du catalogue : {line!r}")
        items_by_title[canonical_title] = items_by_title.get(canonical_title, 0) + 1
    return [CartItem(title=title, quantity=quantity) for title, quantity in items_by_title.items()]
