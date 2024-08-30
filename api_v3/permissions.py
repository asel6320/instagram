from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            if request.user.is_authenticated and request.user == obj.author:
                return True
            else:
                return False
        return True