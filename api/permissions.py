from rest_framework import permissions


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
                request.user.role == request.user.UserRole.ADMIN
        )