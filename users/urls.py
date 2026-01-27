
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentCreateAPIView, PaymentListAPIView, PaymentRetrieveAPIView, RegisterView

app_name = UsersConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),



    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-retrieve'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ] + router.urls