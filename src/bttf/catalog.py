"""Catalogue de la boutique DVD.

Règles de prix du brief :
- un volet de la saga « Back to the Future » coûte 15 € ;
- tout autre film coûte 20 €.

Le catalogue est la seule source de vérité sur les prix : aucune valeur
monétaire n'est dupliquée ailleurs dans le code.
"""

# --- Prix (en euros) ---
SAGA_PRICE: int = 15
OTHER_MOVIE_PRICE: int = 20

# Les trois volets de la saga, identifiés par leur titre exact.
SAGA_TITLES: frozenset[str] = frozenset(
    {
        "Back to the Future 1",
        "Back to the Future 2",
        "Back to the Future 3",
    }
)


def is_saga_movie(title: str) -> bool:
    """True si le titre appartient à la saga « Back to the Future »."""
    return title in SAGA_TITLES


def get_price(title: str) -> int:
    """Prix unitaire d'un film de la boutique.

    Tout titre hors saga est un « autre film » à 20 €, conformément au brief.
    """
    return SAGA_PRICE if is_saga_movie(title) else OTHER_MOVIE_PRICE
