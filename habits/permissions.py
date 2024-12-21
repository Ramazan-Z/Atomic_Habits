from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    """Определение прав владельца привычки"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsPublicHabit(BasePermission):
    """Определение публичности привычки"""

    def has_object_permission(self, request, view, obj):
        return obj.is_public
