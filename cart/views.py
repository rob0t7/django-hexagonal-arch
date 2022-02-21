from typing import Optional

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from cart.models import Cart, CartItems, Product
from cart.serializers import (
    CartItemSerializer,
    CartSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(url_path="items", methods=["POST"], detail=True)
    def add_item(self, request: Request, pk: Optional[str] = None) -> Response:
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(pk=request.data["product_id"])
        try:
            cart_item = cart.items.get(product=product)
            cart_item.quantity += 1
            cart_item.save()
        except CartItems.DoesNotExist:
            CartItems.objects.create(
                cart=cart, product=product, price=product.price, quantity=1
            )
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # @action(url_path="items/<uuid:item_id>", methods=["PATCH"], detail=True)
    # def update_cart_item(
    #     self, request: Request, pk: Optional[str] = None
    # ) -> Response:
    #     cart = self.get_object()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemSerializer
