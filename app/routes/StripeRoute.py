from fastapi import APIRouter, HTTPException
import stripe
import os
from app.schemas.stripeQuoteSchema import QuotesBase, QuotesRequest
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import StreamingResponse
import io


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

stripe_router = APIRouter()


class PaymentRequest(BaseModel):
    paymentIntentId: str

@stripe_router.post("/stripeQuotes")
async def create_quote(quote_request: QuotesRequest, quote_data: QuotesBase):
    try:
        items = quote_request.items  # Extract items from the quote request
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],  # Only card payment allowed for now
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
                        "name": item.name,  # Service name
                        "images": [item.product]  # Product image or identifier
                    },
                    "unit_amount": int(item.price * 100)  # Convert price to cents
                },
                "quantity": item.quantity  # Item quantity
            } for item in items],  # Process all items
            mode="payment",  # Payment mode
            success_url="http://localhost:4100/success.html",  # Success redirect URL
            cancel_url="http://localhost:4100/cancel.html"  # Cancel redirect URL
        )

        return {"session_id": session.id, "quote_id": quote_data.id_usuario}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle any errors that occur


@stripe_router.post("/generate-pdf")
async def generate_pdf(payment_request: PaymentRequest):
    payment_intent_id = payment_request.paymentIntentId

    try:

        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        pdf_buffer = io.BytesIO() 
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        c.setFont("Helvetica", 16)
        c.drawString(100, 750, f"Factura de Pago")
        c.drawString(100, 730, f"ID de Pago: {payment_intent.id}")
        c.drawString(100, 710, f"Monto: ${payment_intent.amount_received / 100}")
        c.drawString(100, 690, f"Cliente: {payment_intent.receipt_email}")
        c.drawString(100, 670, f"Fecha de Pago: {payment_intent.created}")
        c.drawString(100, 650, "¡Gracias por tu compra!")
        
        c.showPage()
        c.save()


        pdf_buffer.seek(0)

        headers = {
            "Content-Disposition": f"attachment; filename=factura_{payment_intent_id}.pdf",
            "Content-Type": "application/pdf",
        }

        return StreamingResponse(pdf_buffer, headers=headers)

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Error con Stripe: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")
