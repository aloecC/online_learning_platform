from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только пользователям из группы 'Модераторы'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Модераторы').exists()