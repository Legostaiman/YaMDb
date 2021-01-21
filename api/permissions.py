from rest_framework import permissions

from users.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or
            obj.author == request.user):
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.role == request.user.Role.ADMIN
        )   


class IsModerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.role == request.user.Role.MODERATOR
        )


class IsAdminOrModerOrUser(permissions.BasePermission):
    def has_object_permission(self, request, view, ojb):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            hasattr(request.user, 'role')
            and request.user.is_staff or
            request.user.role == 'admin' or
            request.user.role == 'moderator'
        )
