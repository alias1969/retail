from http.client import responses

from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Customers, Contacts
from products.models import Products


class PartnersTest(APITestCase):
    """Тест модели Customers"""

    def setUp(self):
        """Исходные данные"""

        Customers.objects.all().delete()
        Contacts.objects.all().delete()
        Products.objects.all().delete()

        # Создаем модели сотрудника и задачи
        self.user = User.objects.create(username="test user")
        self.product = Products.objects.create(name="test product", item="test item")
        self.contact = Contacts.objects.create(
            email="test@test.ru", country="test country", city="test city"
        )
        self.customer = Customers.objects.create(
            name="test customer",
        )
        self.customer.сontacts.add(self.contact)
        self.customer.products.add(self.product)

        # Завод
        self.retail = Customers.objects.create(
            name="test customer", parent=self.customer
        )
        # ИП
        self.entrepreneur = Customers.objects.create(
            name="test customer", parent=self.retail
        )

        self.client.force_authenticate(user=self.user)

    def test_customer_create(self):
        """Тестирование создание контрагента"""

        data = {
            "name": "TEST",
        }
        response = self.client.post("/partners/customer/", data=data)
        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["name"], "TEST")
        self.assertEqual(data_json["level"], 0)
        self.assertEqual(data_json["parent"], None)
        self.assertEqual(data_json["debt_to_supplier"], 0)
        self.assertEqual(data_json["сontacts"], [])
        self.assertEqual(data_json["products"], [])

    def test_customer_list(self):
        """Тест списка всех контрагентов"""

        url = reverse("partners:customer-list")
        response = self.client.get(url)

        # Сверяем код с ожидаемыми
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Сверяем данные с ожидаемыми
        data_json = response.json()[0]

        self.assertEqual(data_json["name"], "test customer")
        self.assertEqual(data_json["debt_to_supplier"], 0.0)
        self.assertEqual(data_json["level"], 0)
        self.assertEqual(len(data_json["сontacts"]), 1)
        self.assertEqual(len(data_json["products"]), 1)
        # Сверяем ожидаемое количество контрагентов в БД
        self.assertEqual(Customers.objects.count(), 1)

    def test_customer_retrieve(self):
        """Тест детальной информации по контрагенту"""

        url = reverse("partners:customer-detail", args=(self.customer.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["name"], "test customer")
        self.assertEqual(data_json["debt_to_supplier"], 0)
        self.assertEqual(len(data_json["сontacts"]), 1)
        self.assertEqual(len(data_json["products"]), 1)

    def test_customer_update(self):
        """Тестирование обновление контрагента"""

        url = reverse("partners:customer-detail", args=(self.customer.pk,))

        data = {
            "name": "test2 customer",
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(Customers.objects.count(), 1)

        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["name"], "test2 customer")

    def test_customer_update_parent(self):
        """Тестирование ссылки контрагента на себя"""

        url = reverse("partners:customer-detail", args=(self.customer.pk,))

        data = {
            "name": "test customer",
            "parent": [self.customer.id],
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_level_retail(self):
        """Тестирование определение уровня контрагента-завода"""

        url = reverse("partners:customer-detail", args=(self.retail.pk,))
        response = self.client.get(url)
        self.assertEqual(response.json()["level"], 1)

    def test_customer_level_entrepreneur(self):
        """Тестирование определение уровня контрагента-ИП"""

        url = reverse("partners:customer-detail", args=(self.entrepreneur.pk,))
        response = self.client.get(url)
        self.assertEqual(response.json()["level"], 2)

    def test_customer_delete(self):
        """Тестирование удаление задачи"""

        url = reverse("partners:customer-detail", args=(self.customer.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Сверяем ожидаемое количество задач
        self.assertEqual(Customers.objects.count(), 0)

    def test_contact_create(self):
        """Тестирование создание контакта"""

        data = {
            "email": "test2@test.ru",
            "country": "test country",
            "city": "test city",
            "street": "test street",
            "apt": "test apt",
        }
        response = self.client.post("/partners/contacts/", data=data)
        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["email"], "test2@test.ru")
        self.assertEqual(data_json["country"], "test country")
        self.assertEqual(data_json["city"], "test city")
        self.assertEqual(data_json["street"], "test street")
        self.assertEqual(data_json["apt"], "test apt")

    def test_contact_list(self):
        """Тест списка всех контактов"""

        url = reverse("partners:contacts-list")
        response = self.client.get(url)
        data = response.json()[0]

        # Сверяем код с ожидаемыми
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем ожидаемое количество контрагентов в БД
        self.assertEqual(Contacts.objects.count(), 1)

    def test_contact_retrieve(self):
        """Тест детальной информации по контакту"""

        url = reverse("partners:contacts-detail", args=(self.contact.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["email"], "test@test.ru")
        self.assertEqual(data_json["country"], "test country")
        self.assertEqual(data_json["city"], "test city")
        self.assertEqual(data_json["street"], None)
        self.assertEqual(data_json["apt"], None)

    def test_contact_update(self):
        """Тестирование обновление контактов"""

        url = reverse("partners:contacts-detail", args=(self.contact.pk,))

        data = {
            "email": "test@test.ru",
            "country": "test country",
            "city": "test city",
            "street": "test street",
            "apt": "1",
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем ожидаемое количество Tracker в БД
        self.assertEqual(Contacts.objects.count(), 1)

        # Сверяем данные с ожидаемыми
        data_json = response.json()
        self.assertEqual(data_json["street"], "test street")
        self.assertEqual(data_json["apt"], "1")

    def test_contact_delete(self):
        """Тестирование удаление контакта"""

        url = reverse("partners:contacts-detail", args=(self.contact.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Сверяем ожидаемое количество задач
        self.assertEqual(Contacts.objects.count(), 0)
