from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from partners.permissions import IsActiveUser
from products.models import Products
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для Product"""

    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("name", "item", "id")
    permission_classes = [IsActiveUser]
