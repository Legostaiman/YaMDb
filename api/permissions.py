from rest_framework import permissions

from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff or
            request.user.role == request.user.Role.ADMIN
        )


class ReviewCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS or
                obj.author == request.user):
            return True
        return (
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user or
            request.user.role == request.user.Role.MODERATOR or
            request.user.role == request.user.Role.ADMIN
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'role') and
            request.user.role == User.Role.ADMIN or
            request.user.is_superuser
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


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )
