from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from partners.models import Customers, Contacts


class CityFilter(SimpleListFilter):
    """Фильтр контрагентов по названию города"""

    title = "Город в контактах"
    parameter_name = "city"

    def lookups(self, request, model_admin):
        """Получаем уникальные города из контактов"""
        cities = Contacts.objects.values_list("city", flat=True).distinct()
        return [(c, c) for c in cities if c]

    def queryset(self, request, queryset):
        """Фильтруем контрагентов, у которых в контактах указан выбранный город"""
        if self.value():
            return queryset.filter(сontacts__city=self.value()).distinct()
        return queryset


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    """Админка контрагентов"""

    list_display = (
        "name",
        "parent_name",
        "debt_to_supplier",
        "create_at",
    )  # ссылку на «Поставщика»
    list_filter = [CityFilter]  # фильтр по названию города

    def display_contacts(self, obj):
        return ", ".join([a.name for a in obj.contacts.all()])

    display_contacts.short_description = "Контакты"

    # admin action - очищающий задолженность
    actions = ["debt_to_supplier_is_null"]

    @admin.action(description="Обнулить задолженность")
    def debt_to_supplier_is_null(self, request, queryset):
        queryset.update(debt_to_supplier=0)
        self.message_user(request, "Задолженность обнулена")

    def parent_name(self, obj):
        """Вывод название поставщика"""
        if obj.parent is None:
            return obj.parent
        return obj.parent.name

    parent_name.short_description = "Поставщик"


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    """Админка контактов"""

    # фильтр по названию города
    list_filter = ("city",)
