from rest_framework.permissions import SAFE_METHODS, BasePermission

from core.models.config import (USER_ROLE_CUSTOMER, USER_ROLE_MODERATOR, USER_ROLE_STAFF)


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'role') and request.user.role == USER_ROLE_CUSTOMER:
            return super().has_permission(request, view)
        return False


class IsCustomerReadOnly(IsCustomer):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return super().has_permission(request, view)
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'role') and request.user.role == USER_ROLE_MODERATOR:
            return super().has_permission(request, view)
        return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'role'):
            staff_flags = (request.user.role == USER_ROLE_STAFF or request.user.is_staff or request.user.is_superuser)
            if staff_flags:
                return super().has_permission(request, view)
        return False
