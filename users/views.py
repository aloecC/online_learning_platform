from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Payment
from users.permisions import IsOwner
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer, UserProfileEditSerializer, \
    UserSerializerForAnother


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'destroy', 'update']:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return UserSerializer  # Для просмотра профиля
        elif self.action in ['update', 'partial_update']:
            return UserProfileEditSerializer  # Для редактирования профиля
        elif self.action == 'list':
            return UserSerializerForAnother
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer_class = self.get_serializer_class()
        if user == request.user:
            serializer = UserSerializer(user)
        else:
            serializer = UserSerializerForAnother(user)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


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