import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeConnectService:

    @staticmethod
    def create_connect_account(user):
        account = stripe.Account.create(
            type="express",
            email=user.email,
        )

        user.stripe_account_id = account.id
        user.save(update_fields=["stripe_account_id"])

        return account

    @staticmethod
    def create_onboarding_link(user):
        link = stripe.AccountLink.create(
            account=user.stripe_account_id,
            refresh_url="http://localhost:8000/reauth",
            return_url="http://localhost:8000/success",
            type="account_onboarding",
        )

        return link.url