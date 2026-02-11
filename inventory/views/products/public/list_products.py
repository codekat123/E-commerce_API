from django.core.cache import cache
from django.db.models import Avg
from rest_framework.generics import ListAPIView

from ....models import Product
from ....serializers import ProductListSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    CACHE_TIMEOUT = 60

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")

        queryset = (
            Product.objects
            .filter(is_active=True, is_archived=False)
            .annotate(avg_stars=Avg("rating__stars"))
            .select_related("category")
            .prefetch_related("images")
            .order_by("-avg_stars")
        )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def list(self, request, *args, **kwargs):
        category_slug = self.kwargs.get("category_slug", "all")
        page_number = request.query_params.get("page", 1)

        cache_key = f"products:list:{category_slug}:page:{page_number}"

        cached_response = cache.get(cache_key)
        if cached_response:
            return self.get_paginated_response(cached_response)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        
        serializer = self.get_serializer(page, many=True)
        cache.set(cache_key, serializer.data, self.CACHE_TIMEOUT)
        return self.get_paginated_response(serializer.data)
        
