from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsRealtor(BasePermission):
    def has_permission(
        self,
        request: Request,
        view: View,
    ) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == "realtor"
        )


class IsAdmin(BasePermission):
    def has_permission(
        self,
        request: Request,
        view: View,
    ) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: object,
    ) -> bool:
        return obj.user == request.user