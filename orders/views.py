from rest_framework.viewsets import ModelViewSet
from .models import Order
from .serializers import OrderSerializer
from orders import serializers


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pass
