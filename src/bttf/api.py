"""Interface HTTP (FastAPI).

Adaptateur mince autour du noyau de domaine : lecture du panier
textuel, délégation au calcul, traduction des erreurs en HTTP.
L'OpenAPI est généré automatiquement sur /docs.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from bttf.cart import compute_price_breakdown
from bttf.parser import CartParsingError, parse_cart

app = FastAPI(
    title="BTTF Cart API",
    description="Calculeur de panier DVD « Back to the Future » — exercice Ekinox.",
    version="0.1.0",
)


class PriceRequest(BaseModel):
    """Corps de requête : le panier saisi sous forme de texte."""

    cart_text: str = Field(..., description="Un titre de film par ligne.", min_length=0)


class PriceResponse(BaseModel):
    """Réponse : total arrondi et détail du calcul."""

    total: int
    breakdown: dict[str, int]


@app.post("/api/price", response_model=PriceResponse)
def compute_price(request: PriceRequest) -> PriceResponse:
    """Calcule le prix d'un panier textuel.

    Raises:
        HTTPException 422: si une ligne référence un film inconnu.
    """
    try:
        items = parse_cart(request.cart_text)
    except CartParsingError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    breakdown = compute_price_breakdown(items)
    return PriceResponse(
        total=breakdown.total,
        breakdown={
            "subtotal": breakdown.subtotal,
            "saga_line_total": breakdown.saga_line_total,
            "other_line_total": breakdown.other_line_total,
            "discount_percent": breakdown.discount_percent,
            "discount_amount": breakdown.discount_amount,
            "total": breakdown.total,
        },
    )


@app.get("/", response_class=HTMLResponse)
def web_page() -> str:
    """La page web minimale (interface du brief)."""
    static_dir = Path(__file__).parent / "static"
    return (static_dir / "index.html").read_text(encoding="utf-8")
