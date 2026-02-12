from django.core.cache import cache
from django.db.models import Avg
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from ....models import Product
from ....serializers import ProductListSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    authentication_classes = []
    permission_classes = []
    CACHE_TIMEOUT = 60

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")

        queryset = (
            Product.objects
            .filter(is_active=True, is_archived=False)
            .annotate(avg_stars=Avg("ratings__stars"))
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
            return Response(cached_response)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            cache.set(cache_key, paginated_response.data, self.CACHE_TIMEOUT)
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
