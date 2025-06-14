import django_filters
from django.db.models import Q

from .models import Customers


class CustomersFilter(django_filters.FilterSet):
    """Фильтр по старне в DRF"""

    countries = django_filters.CharFilter(field_name="contacts__country", lookup_expr="icontains",distinct=True)

    class Meta:
        model = Customers
        fields = []
