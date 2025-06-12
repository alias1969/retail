from django.db import models

NULLABLE = {"blank": True, "null": True}


class Products(models.Model):
    """Модель продуктов"""

    name = models.CharField(
        max_length=250,
        verbose_name="Название продукта",
        help_text="Укажите название продукта",
        **NULLABLE,
    )

    item = models.CharField(
        max_length=150,
        verbose_name="Модель продукта",
        help_text="Укажите модель продукта",
    )

    release_at = models.DateField(
        verbose_name="Дата выхода продукта",
        help_text="Укажите дату выхода продукта",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "продукты"
        ordering = ["name", "release_at"]

    def __str__(self):
        return self.name
