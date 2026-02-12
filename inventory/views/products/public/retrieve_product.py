from rest_framework.generics import RetrieveAPIView
from users.permissions import IsClient , IsAdmin , IsStaff
from ....serializers import ProductRetrieveSerializer
from ....models import Product
from rest_framework.exceptions import ValidationError 

class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [IsClient | IsAdmin | IsStaff]
    lookup_field = 'uuuid'
