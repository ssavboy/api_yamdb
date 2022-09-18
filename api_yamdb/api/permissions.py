from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Этот класс используется для определения
    кастомных полномочий для разрешения редактирования, удаления
    объекта автором, модератором, администритором.
    """

    def has_object_permission(self, request, view, obj):
        """Разрешение на редактирование, удаление объекта."""
        return (
            obj.author == request.user or request.user.is_moderator
            or request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )
class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
