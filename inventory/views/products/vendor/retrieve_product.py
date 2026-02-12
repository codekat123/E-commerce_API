from rest_framework.generics import RetrieveAPIView
from ....serializers import ProductVendorRetrieveSerializer
from ....models import Product 
from users.permissions import IsVendor

class ProductVendorRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductVendorRetrieveSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        return (
            Product.objects
            .filter(
                vendor=self.request.user
            )
        )