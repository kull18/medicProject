from fastapi import APIRouter, HTTPException
import stripe
import os
from app.schemas.stripeQuoteSchema import QuotesBase, QuotesRequest

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

stripe_router = APIRouter()

@stripe_router.post("/stripeQuotes")
async def create_quote(quote_request: QuotesRequest, quote_data: QuotesBase):
    try:
        items = quote_request.items

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            shipping_address_collection={
                "allowed_countries": ["US", "MX"]
            },
            shipping_options=[{
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {
                        "amount": 0,
                        "currency": "mxn"
                    },
                    "display_name": "Free shipping",
                    "delivery_estimate": {
                        "minimum": {
                            "unit": "business_day",
                            "value": 5
                        },
                        "maximum": {
                            "unit": "business_day",
                            "value": 7
                        }
                    }
                }
            }, {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {
                        "amount": 1500,
                        "currency": "mxn"
                    },
                    "display_name": "Next day air",
                    "delivery_estimate": {
                        "minimum": {
                            "unit": "business_day",
                            "value": 1
                        },
                        "maximum": {
                            "unit": "business_day",
                            "value": 1
                        }
                    }
                }
            }],
            line_items=[{
                "price_data": {
                    "currency": "mxn",
                    "product_data": {
                        "name": item.name,
                        "images": [item.product]
                    },
                    "unit_amount": int(item.price * 100)  # Convertir a centavos
                },
                "quantity": item.quantity
            } for item in items],
            mode="payment",
            success_url="http://localhost:4100/success.html",
            cancel_url="http://localhost:4100/cancel.html"
        )

        return {"session_id": session.id, "quote_id": quote_data.id_usuario}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

