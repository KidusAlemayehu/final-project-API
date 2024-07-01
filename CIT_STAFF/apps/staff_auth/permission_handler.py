from rest_framework.permissions import BasePermission
from apps.staff_user.models import OfficeChoices, RoleChoices

class IsAuthenticated(BasePermission):
    message = "Permission Denied, Authenticated Users Only"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated

class IsHOD(BasePermission):
    message = "Permission Denied, Allowed for HOD Only"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.HOD, role=RoleChoices.ADMINISTRATOR).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.HOD, role=RoleChoices.ADMINISTRATOR).exists()

class IsUGSectionHead(BasePermission):
    message = "Permission Denied, UG Section Head Only"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.UG, role=RoleChoices.HEAD).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.UG, role=RoleChoices.HEAD).exists()

class IsUGStaff(BasePermission):
    message = "Permission Denied, UG Staff Only"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.UG, role=RoleChoices.STAFF).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.UG, role=RoleChoices.STAFF).exists()

class IsPGStaff(BasePermission):
    message = "Permission Denied, PG Staff Only"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.PG, role=RoleChoices.STAFF).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.PG, role=RoleChoices.STAFF).exists()

class IsPGCoordinator(BasePermission):
    message = "Permission Denied, PG Coordinator Only"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.PG, role=RoleChoices.COORDINATOR).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.roles.filter(office__name=OfficeChoices.PG, role=RoleChoices.COORDINATOR).exists()

class IsAdministrator(BasePermission):
    message = "Permission Denied, Administrators Only (Developer and HOD)"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(office__name__in=[OfficeChoices.DEVELOPER, OfficeChoices.HOD], role=RoleChoices.ADMINISTRATOR).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.roles.filter(office__name__in=[OfficeChoices.DEVELOPER, OfficeChoices.HOD], role=RoleChoices.ADMINISTRATOR).exists()
