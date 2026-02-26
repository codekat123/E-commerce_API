from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeDepositService:

    @staticmethod
    def create_deposit_session(amount, user):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Wallet Deposit",
                        },
                        "unit_amount": int(amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
            metadata={
                "type": "deposit",
                "user_id": user.id,
            }
        )

        return session