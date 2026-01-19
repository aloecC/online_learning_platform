from os import path

from django.urls import include, path

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
app_name = UsersConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [

] + router.urls