from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from partners.filters import CustomersFilter
from partners.models import Customers, Contacts
from partners.permissions import IsActiveUser
from partners.serializers import CustomerSerializer, ContactSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet для Customer"""

    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_classs = CustomersFilter
    permission_classes = [IsActiveUser]
    ordering_fields = ("name", "id")


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet для Customer"""

    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    permission_classes = [IsActiveUser]
