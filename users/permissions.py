from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.is_superuser


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'user'


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
