from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Необходим для того, чтобы рецепт мог обновить
    только его автор или админ.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or obj.author == request.user)
