from .models import Product
from rest_framework.exceptions import ValidationError
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector
)



class SearchService:

    @staticmethod
    def search_query(query):

        search_query = SearchQuery(query)

        vector_search = (
            SearchVector('name', weight='A') +
            SearchVector('category__name', weight='B') +
            SearchVector('description', weight='C')
        )

        products = Product.objects.annotate(
            rank=SearchRank(vector_search, search_query)
        ).filter(
            rank__gte=0.1
        ).order_by('-rank')

        if len(products) == 0:
            raise ValidationError({'detail':f'there are no proaducts for {query}'})
        else:
            return products