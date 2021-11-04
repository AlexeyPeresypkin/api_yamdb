from rest_framework import permissions


class ReviewOrCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
                obj.author == request.user or
                request.method in permissions.SAFE_METHODS or
                request.user.role == request.user.UserRole.MODERATOR or
                request.user.role == 'admin')


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user.is_staff or
                request.user.role == 'admin'
        )
