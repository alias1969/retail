from rest_framework import serializers
from partners.permissions import IsActiveUser
from partners.models import Customers, Contacts


class CustomerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Customers"""

    debt_to_supplier = serializers.FloatField(read_only=True)

    level = serializers.SerializerMethodField(read_only=True)

    def get_level(self, obj):
        """Метод для определения уровня контрагента"""
        if obj.parent:
            if obj.parent.parent:
                # если заполнен родитель в родителе, то уровень = 2 (индивидуальный предприниматель)
                return 2
            else:
                # если в родителе не заполнен родитель, то уровень = 1 (розничная сеть)
                return 1
        # если не заполнен родитель, то уровень = 0 (завод)
        return 0

    def validate_parent(self, value):
        """Проверка поле Поставщик - нельзя ссылать на самого себя"""
        if value and self.instance.pk == value.pk:
            raise serializers.ValidationError(
                "Контрагент не может ссылаться сам на себя"
            )
            return value

    class Meta:
        model = Customers
        fields = "__all__"
        permission_classes = [IsActiveUser]


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор для Contact"""

    class Meta:
        model = Contacts
        fields = "__all__"
        permission_classes = [IsActiveUser]
