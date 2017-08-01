from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated


class IsOwnerAccountOrReadOnly(BasePermission):
    """Custom permission for the owner of the account.

    Write permissions only to the owner of the account, otherwise only
    GET, OPTIONS AND HEAD requests are allowed.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and is_authenticated(request.user) and
            int(view.kwargs['pk']) == request.user.id
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerObjectOrReadOnly(BasePermission):
    """Custom permission for the owner of the object.

    Write permission only to the owner of the object, otherwise only
    GET, OPTIONS AND HEAD requests are allowed.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            request.user and is_authenticated(request.user) and
            obj.user_id == request.user.id
        )
