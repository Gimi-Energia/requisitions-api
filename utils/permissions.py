from rest_framework import permissions


class IsAuthenticatedGet(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_authenticated or request.user.is_staff)


class IsAdminPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.method == "POST"


class AllowAnyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class IsAdminGet(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
