from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart, CartItems
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    ProductSerializer,
    Product,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(url_path="items", methods=["POST"], detail=True)
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

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
