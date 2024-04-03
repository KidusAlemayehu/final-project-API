from rest_framework.permissions import BasePermission
    
class IsAuthenticated(BasePermission):
    message = "Permission Denied, Authenticated Users Only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated
    
class IsHOD(BasePermission):
    message = "Permission Denied, Allowed for HOD Only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == 'Head of Department'
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == 'Head of Department'
    
class IsUGStaff(BasePermission):
    message = "Permission Denied, UG staff only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == "Under-Graduate" and request.user.role == "Staff"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == "Under-Graduate" and request.user.role == "Staff"
    
class IsUGCoordinator(BasePermission):
    message = "Permission Denied, UG Coordinator only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == "Under-Graduate" and request.user.role == "Coordinator"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == "Under-Graduate" and request.user.role == "Coordinator"
    
class IsPGStaff(BasePermission):
    message = "Permission Denied, PG staff only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == "Post-Graduate" and request.user.role == "Staff"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == "Post-Graduate" and request.user.role == "Staff"
    
class IsPGCoordinator(BasePermission):
    message = "Permission Denied, PG Coordinator only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == "Post-Graduate" and request.user.role == "Coordinator"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == "Post-Graduate" and request.user.role == "Coordinator"   

class IsTAStaff(BasePermission):
    message = "Permission Denied, TA staff only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == "Technical Assistant" and request.user.role == "Staff"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == "Technical Assistant" and request.user.role == "Staff"
    
class IsTACoordinator(BasePermission):
    message = "Permission Denied, TA Coordinator only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.office == "Technical Assistant" and request.user.role == "Coordinator"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.office == "Technical Assistant" and request.user.role == "Coordinator"     