from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя"""
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_payments(self, obj):
        payments = obj.payments.order_by('payment_date')
        return PaymentSerializer(payments, many=True).data


class UserSerializerForAnother(serializers.ModelSerializer):
    """Сериализатор модели пользователя для посторонних"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email',]


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']  # Поля для редактирования
        extra_kwargs = {'password': {'write_only': True}}  # Пароль только для записи


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Храните пароль в зашифрованном виде
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежей"""

    class Meta:
        model = Payment
        fields = '__all__'

