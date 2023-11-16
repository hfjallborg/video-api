from rest_framework import permissions

from .models import Video


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allows safe methods for non-owner."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class VideoStatusPermission(permissions.BasePermission):
    """Allows access for public videos"""

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True
        elif obj.user == request.user:
            if obj.status == Video.Status.DELETED:
                # Only staff has access to "deleted" videos
                return False
            return True
        elif obj.status == Video.Status.PUBLIC:
            if request.method in permissions.SAFE_METHODS:
                return True
        return False
