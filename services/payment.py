import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:

    @staticmethod
    def create_checkout_session(order, user):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Order #{order.id}"
                        },
                        "unit_amount": int(order.total_price * 100),
                    },
                    "quantity": 1,
                }
            ],
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            metadata={
                "order_id": order.id,
                "user_id": user.id,
            }
        )

        return session