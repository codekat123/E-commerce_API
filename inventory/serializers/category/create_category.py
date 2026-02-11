from rest_framework import serializers
from ...models import Category


class CategoryCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name','description']
        