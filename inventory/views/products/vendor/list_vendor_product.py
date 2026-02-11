from rest_framework.generics import ListAPIView
from users.permissions import IsVendor
from ....serializers import ProductVendorListSerializer
from ....models import Product




class ProductVendorListAPIView(ListAPIView):
    serializer_class = ProductVendorListSerializer
    permission_classes = [IsVendor]


    def get_queryset(self):
        return (
            Product.objects
            .filter(
                vendor=self.request.user
            )
            .order_by('-created_at')
        )