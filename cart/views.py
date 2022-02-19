from rest_framework import viewsets

from .serializers import ProductSerializer, Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
