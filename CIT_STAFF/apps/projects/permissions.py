from rest_framework.permissions import BasePermission
from .models import ProjectAccessRoleTable, ProjectAccessTable, Project
from django.db.models import Q



### Task Related permissions
class CreateDeleteTaskPermission(BasePermission):
    message = "Permission Denied, Allowed For Project Owner Or Contributor Personnels Only"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role == "Owner" or role_table.access_role == "Contributor":
            return True
        return False
    
class IsProjectContributor(BasePermission):
    message = "Permission Denied, Allowed For Project Contributor Only"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user, access_role="Contributor").first()
        if role_table:
            return True
        return False

class IsProjectCommenter(BasePermission):
    message = "Permission Denied, Allowed For Project Commenter Only"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user, access_role="Commenter").first()
        if role_table:
            return True
        return False
        
class IsProjectViewer(BasePermission):
    message = "Permission Denied, Allowed For Project Viewer Only"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user, access_role="Viewer").first()
        if role_table:
            return True
        return False    
    
        