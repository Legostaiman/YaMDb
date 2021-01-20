from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from users.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or
            obj.author == request.user):
            return True


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'user'


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or request.user.is_superuser

class TitlePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or request.user.is_superuser