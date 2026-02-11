from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView
)
from ..serializers import ProductRatingSerializer
from ..models import ProductRating
from rest_framework.exceptions import ValidationError
from users.permissions import IsClient

class ProductRatingListAPIView(ListAPIView):
    serializer_class = ProductRatingSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        try:
            product_uuid = self.kwargs['uuid']
        except KeyError:
            raise ValidationError("you must add product uuid into url")
            
        return ProductRating.objects.filter(
            product__uuid=product_uuid
        )

class ProductRatingCreateAPIView(CreateAPIView):
    serializer_class = ProductRatingSerializer
    permission_classes = [IsClient] 

    def perform_create(self,serializer):
        product_uuid = self.kwargs.get('uuid')
        if not product_uuid:
            raise ValidationError('you must add uuid into url')
        serializer.save(
            customer=self.request.user,
            product__uuid=product_uuid
        )

class ProductRatingUpdateAPIView(UpdateAPIView):
    serializer_class = ProductRatingSerializer
    permission_classes = [IsClient] 
    
    def get_queryset(self):
        return ProductRating.objects.filter(
            customer=self.request.user
        ) 

class ProductRatingDeleteAPIView(DestroyAPIView):
    serializer_class = ProductRatingSerializer
    permission_classes = [IsClient] 

    def get_queryset(self):
        return ProductRating.objects.filter(
            customer=self.request.user
        )

