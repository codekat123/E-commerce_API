import sib_api_v3_sdk
import os



class BrevoEmailService:
    def __init__(self):
        config = sib_api_v3_sdk.Configuration()
        config.api_key['api-key'] = os.getenv('BREVO_API_KEY')
        self.api = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(config)
        )

    def send(self,to_email,subject,html):
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{'email': to_email}],
            subject=subject,
            html_content=html,
            sender={'email': os.getenv('BREVO_SENDER_EMAIL')}
        )