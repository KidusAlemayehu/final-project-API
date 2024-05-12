from rest_framework.permissions import BasePermission
from .models import ProjectAccessRoleTable, ProjectAccessTable, Project
from django.db.models import Q



### Task Related permissions
class CreatePermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a create action!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role == "Owner" or role_table.access_role == "Contributor":
            return True
        return False
    
class ReadPermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a view action!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table:
            return True
        return False
    
class UpdatePermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform an update action!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role == "Owner" or role_table.access_role == "Contributor":
            return True
        return False
    
class DeletePermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a delete action!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role == "Owner" or role_table.access_role == "Contributor":
            return True
        return False
    
class ProjectDeletePermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a delete action on this project!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role == "Owner":
            return True
        return False
    
class CommentCreatePermission(BasePermission):
    message = "Permission Denied: You are not allowed to write a comment!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role == "Owner" or role_table.access_role == "Contributor" or role_table.access_role == "Commenter":
            return True
        return False    
 
class CommentReadPermission(BasePermission):
    message = "Permission Denied: You are not allowed to read this comment!"

    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table:
            return True
        return False   

class CommentUpdatePermission(BasePermission):
    message = "Permission Denied: You are not allowed to Update this comment!"

    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        comment = view.get_object()
        
        if role_table.access_role == "Commenter" and comment.objects.filter(pk=view.kwargs.get('comment_pk'), commented_by=request.user).exists():
            return True
        return False 

class CommentDeletePermission(BasePermission):
    message = "Permission Denied: You are not allowed to Delete this comment!"

    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        comment = view.get_object()
        
        if role_table.access_role == "Owner":
            return True
        elif role_table.access_role == "Commenter" and comment.objects.filter(pk=view.kwargs.get('comment_pk'), commented_by=request.user).exists():
            return True
        return False   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
 
# class IsProjectContributor(BasePermission):
#     message = "Permission Denied, Allowed For Project Contributor Only"
    
#     def has_permission(self, request, view):
#         project_pk = view.kwargs.get('project_pk')
#         project = Project.objects.filter(pk=project_pk).first()
#         role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user, access_role="Contributor").first()
#         if role_table:
#             return True
#         return False

# class IsProjectCommenter(BasePermission):
#     message = "Permission Denied, Allowed For Project Commenter Only"
    
#     def has_permission(self, request, view):
#         project_pk = view.kwargs.get('project_pk')
#         project = Project.objects.filter(pk=project_pk).first()
#         role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user, access_role="Commenter").first()
#         if role_table:
#             return True
#         return False
        
# class IsProjectViewer(BasePermission):
#     message = "Permission Denied, Allowed For Project Viewer Only"
    
#     def has_permission(self, request, view):
#         project_pk = view.kwargs.get('project_pk')
#         project = Project.objects.filter(pk=project_pk).first()
#         role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user, access_role="Viewer").first()
#         if role_table:
#             return True
#         return False    
    
        