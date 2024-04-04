from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows full access only to owner, read only otherwise. 
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsAdminOrReadOnly():
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
