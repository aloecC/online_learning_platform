from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    '''Разрешение на доступ владельцу'''

    def has_permission(self, request, view):
        return request.user == view.get_object()



