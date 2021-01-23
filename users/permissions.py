from rest_framework import permissions

from .models import User


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'role') and
            request.user.role == User.Role.ADMIN or request.user.is_superuser
            )


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'role') and
            request.user.role == User.Role.MODERATOR
            )


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'role') and
            request.user.role == User.Role.USER
            )


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.email == request.user or
            request.method in permissions.SAFE_METHODS
            )
