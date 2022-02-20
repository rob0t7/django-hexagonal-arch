from rest_framework import serializers

from .models import Cart, CartItems, Product


class ProductSerializer(serializers.ModelSerializer[Product]):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "price",
        ]


class CartItemSerializer(serializers.ModelSerializer[CartItems]):
    product_id = serializers.UUIDField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    quantity = serializers.IntegerField(default=1)
    # name = serializers.CharField(read_only=True)

    class Meta:
        model = CartItems
        fields = ["product_id", "price", "quantity", "product_name"]


class CartSerializer(serializers.ModelSerializer[Cart]):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]
