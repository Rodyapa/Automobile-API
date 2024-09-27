from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrIsStaffOrReadOnly(BasePermission):
    """Only owner of object can edit it."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_active
                and (request.user == obj.owner or request.user.is_staff)
                )
