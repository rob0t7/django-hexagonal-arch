from rest_framework import serializers
from . import models


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ["quantity", "price", "name"]


class OrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(read_only=True)

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = [
            "order_number",
            "order_date",
            "id",
            "customer_id",
            "items",
        ]
