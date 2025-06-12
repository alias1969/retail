from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Products
from datetime import date, datetime

from django.contrib.auth.models import User

TRACKER_DATETIME = date.today()
TRACKER_DATETIME_STR = date.today().strftime("%Y-%m-%d")


class ProductTest(APITestCase):
    """Тест модели Customers"""

    def setUp(self):
        """Исходные данные"""

        Products.objects.all().delete()

        # Создаем модели сотрудника и задачи
        self.user = User.objects.create(username="test user")
        self.product = Products.objects.create(
            name="test product", item="test item", release_at=TRACKER_DATETIME
        )

        self.client.force_authenticate(user=self.user)

    def test_product_create(self):
        """Тестирование создание продукта"""

        data = {
            "name": "test2 product",
            "item": "test2 item",
            "release_at": TRACKER_DATETIME,
        }
        response = self.client.post("/products/", data=data)
        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["name"], "test2 product")
        self.assertEqual(data_json["item"], "test2 item")
        self.assertEqual(data_json["release_at"], TRACKER_DATETIME_STR)

    def test_products_list(self):
        """Тест списка всех продуктов"""

        url = reverse("products:products-list")
        response = self.client.get(url)

        # Сверяем код с ожидаемыми
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем ожидаемое количество контрагентов в БД
        self.assertEqual(Products.objects.count(), 1)

    def test_product_retrieve(self):
        """Тест детальной информации по продукту"""

        url = reverse("products:products-detail", args=(self.product.pk,))
        response = self.client.get(url)

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["name"], "test product")
        self.assertEqual(data_json["item"], "test item")
        self.assertEqual(data_json["release_at"], TRACKER_DATETIME_STR)

    def test_product_update(self):
        """Тестирование обновление продукта"""

        url = reverse("products:products-detail", args=(self.product.pk,))

        data = {
            "name": "test2 product",
            "item": "test2 item",
            "release_at": TRACKER_DATETIME,
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(Products.objects.count(), 1)

        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["name"], "test2 product")
        self.assertEqual(data_json["item"], "test2 item")
        self.assertEqual(data_json["release_at"], TRACKER_DATETIME_STR)

    def test_product_delete(self):
        """Тестирование удаление продукта"""

        url = reverse("products:products-detail", args=(self.product.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Сверяем ожидаемое количество задач
        self.assertEqual(Products.objects.count(), 0)
