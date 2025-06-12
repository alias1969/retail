import django_filters
from .models import Customers


class CustomersFilter(django_filters.FilterSet):
    """Фильтр по старне в DRF"""

    country_name = django_filters.CharFilter(
        field_name="country_name", lookup_expr="icontains"
    )

    class Meta:
        model = Customers
        fields = []
