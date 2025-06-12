from django.db import models
from products.models import Products

NULLABLE = {"blank": True, "null": True}


class Contacts(models.Model):
    """Модель контактов контрагентов"""

    email = models.EmailField(
        unique=True,
        verbose_name="email",
        help_text="Введите email",
        **NULLABLE,
    )

    country = models.CharField(
        max_length=150,
        verbose_name="Страна",
        help_text="Укажите старну",
        **NULLABLE,
    )

    city = models.CharField(
        max_length=150,
        verbose_name="Город",
        help_text="Укажите город",
        **NULLABLE,
    )

    street = models.CharField(
        max_length=250,
        verbose_name="Улица",
        help_text="Укажите улицу",
        **NULLABLE,
    )

    apt = models.CharField(
        max_length=250,
        verbose_name="Номер дома",
        help_text="Укажите номер дома",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.email}, {self.country}"


class Customers(models.Model):
    """Модель сети контрагентов"""

    name = models.CharField(
        max_length=250,
        verbose_name="Наименование контрагента",
        help_text="Введите название контрагента",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Поставщик",
        help_text="Укажите связанного поставщика",
        **NULLABLE,
    )

    debt_to_supplier = models.FloatField(
        verbose_name="Задолженность перед поставщиком",
        help_text="Введите задолженность перед поставщиком",
        **NULLABLE,
        default=0,
    )

    create_at = models.DateTimeField(
        verbose_name="Время создания",
        auto_now_add=True,
    )

    сontacts = models.ManyToManyField(
        Contacts,
        verbose_name="Контакты",
        help_text="выберите контакты",
        **NULLABLE,
    )

    products = models.ManyToManyField(
        Products,
        verbose_name="Продукты",
        help_text="выберите продукты",
        related_name="products",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["name"]

    def __str__(self):
        return self.name
