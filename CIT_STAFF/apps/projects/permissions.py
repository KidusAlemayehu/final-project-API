from rest_framework.permissions import BasePermission
from .models import ProjectAccessRoleTable, ProjectAccessTable, Project, ProjectTaskAssignment
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
    
class ListPermission(BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role in ['Owner', 'Contributor', 'Commenter', 'Viewer']:
            return True
        return False
        
class ReadPermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a view action!"
    
    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk')
        project = Project.objects.filter(pk=project_pk).first()
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=project, user=request.user).first()
        if role_table.access_role in ['Owner', 'Contributor', 'Commenter', 'Viewer']:
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
        task_pk = view.kwargs.get('pk')
        if task_pk:
            is_task_assignee = ProjectTaskAssignment.objects.filter(
                task__pk=task_pk,
                assignee=request.user
            ).exists()

            if is_task_assignee:
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
    
    
class ProjectListPermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a view action!"
    
    def has_permission(self, request, view):
        # If the user is not authenticated, deny permission
        if not request.user.is_authenticated:
            return False
        
        # Get the user's roles from the ProjectAccessRoleTable
        user_roles = ProjectAccessRoleTable.objects.filter(user=request.user)
        
        # Get the project ids associated with the user's roles
        project_ids = user_roles.values_list('project_access_table__project__pk', flat=True)
        
        # Filter projects based on the user's roles
        projects = Project.objects.filter(pk__in=project_ids)
        
        # If the user has access to any projects, allow permission
        return projects.exists()
        
class ProjectDeletePermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a delete action on this project!"
    
    def has_permission(self, request, view):
        role_table = ProjectAccessRoleTable.objects.filter(project_access_table__project=view.get_object(), user=request.user, access_role='Owner').first()
        if role_table:
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
        
        if comment.commented_by == request.user:
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
    
        