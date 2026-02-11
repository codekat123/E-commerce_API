from rest_framework.viewsets import ModelViewSet
from users.permissions import IsAdmin
from rest_framework.permissions import AllowAny
from ..models import Category
from ..serializers import (
    CategoryReadSerializer,
    CategoryCreationSerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CategoryReadSerializer
        return CategoryCreationSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin]
        return [AllowAny]
