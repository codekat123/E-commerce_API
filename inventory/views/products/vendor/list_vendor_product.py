from rest_framework.generics import ListAPIView


from users.permissions import IsVendor
from ....models import Product
from ....serializers import ProductVendorListSerializer


class ProductVendorListAPIView(ListAPIView):


    serializer_class = ProductVendorListSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        user = self.request.user

        return (
            Product.objects
            .filter(
                vendor=user
            )
            .select_related("category")   
            .prefetch_related("images")   
            .order_by("-created_at")
        )
