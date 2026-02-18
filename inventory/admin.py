from django.contrib import admin
from .models import Product, Category, ProductImage , ProductRating


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'price', 'quantity', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'is_primary', 'created_at')
    search_fields = ('product__name',)
    ordering = ('id',)

@admin.register(ProductRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'comment', 'stars', 'created_at')
    search_fields = ('product__name', 'customer__email')
    ordering = ('-id',)


