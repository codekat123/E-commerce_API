from ..base_register import BaseRegisterSerializer
from ...models import Client 


class ClientRegisterSerializer(BaseRegisterSerializer):
    class Meta:
        model = Client