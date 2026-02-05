from ..base_register import BaseRegisterSerializer
from ...models import Vendor 


class VendorRegisterSerializer(BaseRegisterSerializer):
    class Meta:
        model = Vendor