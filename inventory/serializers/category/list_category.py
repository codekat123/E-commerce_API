from rest_framework import serializers
from ...models import Category


class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("slug", "name")
        read_only_fields = fields
