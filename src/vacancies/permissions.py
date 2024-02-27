from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class VacancyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return True

        return False


class VacancyObjPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH" and request.user == obj.company.owner:
            return True
        if request.method == "DELETE":
            return bool(request.user == obj.company.owner or request.user.is_staff)
        return False
