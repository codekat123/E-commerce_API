from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError 
from ..serializers import ProductListSerializer
from ..services import SearchService


class SearchProductListAPIView(ListAPIView):

    serializer_class = ProductListSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        query = self.request.query_params.get('q')

        if not query:
            raise ValidationError({'detail': 'Search query is required.'})

        return SearchService.search_query(query)
