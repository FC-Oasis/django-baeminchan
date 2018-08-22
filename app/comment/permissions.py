from rest_framework import permissions

__all__ = (
    'IsAuthenticatedOrReadOnly',
    'IsOwnerOrReadOnly',
)


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
