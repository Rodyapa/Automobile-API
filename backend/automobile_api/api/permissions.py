from rest_framework.permissions import SAFE_METHODS, BasePermission


class BaseOwnerOrAuthorOrStaffPermission(BasePermission):
    """Base permission class for owner/author or staff-based permissions."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and self.is_owner_or_author_or_staff(request, obj)
        )

    def is_owner_or_author_or_staff(self, request, obj):
        """Override this method in subclasses to check for owner or author."""
        raise NotImplementedError("Subclasses must implement this method")


class IsOwnerOrIsStaffOrReadOnly(BaseOwnerOrAuthorOrStaffPermission):
    """Only owner of the object or staff can edit it."""

    def is_owner_or_author_or_staff(self, request, obj):
        return request.user == obj.owner or request.user.is_staff


class IsAuthorOrIsStaffOrReadOnly(BaseOwnerOrAuthorOrStaffPermission):
    """Only author of the object or staff can edit it."""

    def is_owner_or_author_or_staff(self, request, obj):
        return request.user == obj.author or request.user.is_staff
