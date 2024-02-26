from rest_framework.permissions import BasePermission

class IsAdministrator(BasePermission):
    
    message="Permission Denied, For Administrators Only"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Administrator'
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'Administrator'
    
class IsStaff(BasePermission):
    
    message="Permission Denied, For Staff Only"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Staff'
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'Staff'
    
class IsResearcher(BasePermission):
    
    message="Permission Denied, For Researcher Only"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Researcher'
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'Researcher'
    
class IsAssistant(BasePermission):
    
    message="Permission Denied, For Assistant Only"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Assistant'
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'Assistant'
    
class IsAuthenticated(BasePermission):
    message = "Permission Denied, Authenticated Users Only"
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated