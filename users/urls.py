from os import path

from django.urls import include, path

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-retrieve'),
    ] + router.urls