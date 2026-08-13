from rest_framework import permissions


class IsVendorOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can read. Only the vendor who owns the product (or superuser) can edit/delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            getattr(request.user, "role", None) == "vendor" or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.vendor == request.user or request.user.is_superuser