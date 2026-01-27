from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Доступ для всех

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": UserSerializer(user).data}, status=201)
        return Response(serializer.errors, status=400)


class TokenObtainPairView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
    filterset_fields = ('course', 'lesson', 'payment_method')  # Набор полей для фильтрации
    ordering_fields = ('payment_date',)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр платежа"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()