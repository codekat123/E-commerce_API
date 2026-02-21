from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsClient
from .serializers import CartSerializer
from .service import CartService


class CartView(APIView):
    permission_classes = [IsClient]

    def get(self, request):
        cart = CartService.get_cart(request.user)
        return Response(cart, status=status.HTTP_200_OK)

    def delete(self, request):
        CartService.clear_cart(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = CartService.add_product(
            user=request.user,
            product_uuid=serializer.validated_data["product_uuid"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = CartService.update_product(
            user=request.user,
            product_uuid=serializer.validated_data["product_uuid"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = CartService.remove_product(
            user=request.user,
            product_uuid=serializer.validated_data["product_uuid"],
        )

        return Response(data, status=status.HTTP_200_OK)
        

class CheckoutView(APIView):
    permission_classes = [IsClient]

    def post(self, request):
        data = CartService.checkout(request.user)
        return Response(data, status=status.HTTP_200_OK)