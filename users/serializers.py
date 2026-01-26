from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_payments(self, obj):
        payments = obj.payments.order_by('payment_date')
        return PaymentSerializer(payments, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежей"""

    class Meta:
        model = Payment
        fields = '__all__'

