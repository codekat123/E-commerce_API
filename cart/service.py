import json
from decimal import Decimal

from django.db import transaction
import redis
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from inventory.models import Product


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


class CartService:

    @staticmethod
    def _get_key(user):
        return f"cart:{user.id}"

    @staticmethod
    def _serialize(cart: dict) -> str:
        return json.dumps(cart)

    @staticmethod
    def _deserialize(data: str | None) -> dict:
        if not data:
            return {}
        return json.loads(data)


    @classmethod
    def get_cart(cls, user) -> dict:
        data = redis_client.get(cls._get_key(user))
        return cls._deserialize(data)

    @classmethod
    def save_cart(cls, user, cart: dict) -> None:
        redis_client.set(
            cls._get_key(user),
            cls._serialize(cart)
        )

    @classmethod
    def clear_cart(cls, user) -> None:
        redis_client.delete(cls._get_key(user))


    @classmethod
    def add_product(cls, user, product_uuid, quantity: int) -> dict:

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        product = get_object_or_404(Product, uuid=product_uuid)

        if product.quantity < quantity:
            raise ValidationError("Not enough stock available.")

        cart = cls.get_cart(user)
        product_id = str(product.uuid)

        if product_id in cart:
            cart[product_id]["quantity"] += quantity
        else:
            cart[product_id] = {
                "name": product.name,
                "price": float(product.price),
                "quantity": quantity,
            }

        cls.save_cart(user, cart)
        return cls._build_summary(cart)

    @classmethod
    def update_product(cls, user, product_uuid, quantity: int) -> dict:

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        product = get_object_or_404(Product, uuid=product_uuid)

        cart = cls.get_cart(user)
        product_id = str(product.uuid)

        if product_id not in cart:
            raise ValidationError("Product not found in cart.")

        if product.quantity < quantity:
            raise ValidationError("Not enough stock available.")

        cart[product_id]["quantity"] = quantity

        cls.save_cart(user, cart)
        return cls._build_summary(cart)

    @classmethod
    def remove_product(cls, user, product_uuid) -> dict:

        cart = cls.get_cart(user)
        product_id = str(product_uuid)

        if product_id not in cart:
            raise ValidationError("Product not found in cart.")

        del cart[product_id]

        cls.save_cart(user, cart)
        return cls._build_summary(cart)


    @staticmethod
    def _build_summary(cart: dict) -> dict:

        total_price = Decimal("0.00")

        for item in cart.values():
            item_total = Decimal(str(item["price"])) * item["quantity"]
            total_price += item_total

        return {
            "items": cart,
            "total_price": float(total_price),
        }


    @classmethod
    @transaction.atomic
    def checkout(cls, user) -> dict:
        cart = cls.get_cart(user)

        if not cart:
            raise ValidationError("Cart is empty.")

        product_ids = list(cart.keys())
        products = Product.objects.select_for_update().filter(uuid__in=product_ids)

        products_map = {str(product.uuid): product for product in products}

        order_items = []
        total_price = Decimal("0.00")

        for product_id, item in cart.items():
            if product_id not in products_map:
                raise ValidationError("Some products no longer exist.")

            product = products_map[product_id]
            quantity = item["quantity"]

            if product.quantity < quantity:
                raise ValidationError(f"Not enough stock for {product.name}.")

            product.quantity -= quantity
            product.save(update_fields=["quantity"])

            item_total = product.price * quantity
            total_price += item_total

            order_items.append({
                "product_uuid": str(product.uuid),
                "quantity": quantity,
                "price": product.price,
            })

        cls.clear_cart(user)

        return {
            "items": order_items,
            "total_price": float(total_price),
        }
