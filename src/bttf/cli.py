"""Interface en ligne de commande.

Usage :
    echo "Back to the Future 1" | python -m bttf.cli
    python -m bttf.cli < panier.txt
"""

import sys

from bttf.cart import compute_order_total
from bttf.parser import CartParsingError, parse_cart


def main() -> int:
    """Lit le panier sur stdin, imprime le prix total sur stdout."""
    cart_text = sys.stdin.read()
    try:
        items = parse_cart(cart_text)
    except CartParsingError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 2
    print(compute_order_total(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
