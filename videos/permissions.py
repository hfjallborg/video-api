from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allows safe methods for non-owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
