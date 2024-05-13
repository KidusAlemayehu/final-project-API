from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from apps.staff_auth import permission_handler as AuthPermissions
import apps.projects.permissions as ProjectPermission
from apps.staff_user.models import StaffUser

# Create your views here.
class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_serializer_context(self):
        user = StaffUser.objects.filter(pk=self.request.user.pk).first()
        context = super().get_serializer_context()
        context['owner'] = user
        return context
    
    def get_queryset(self):
        # Get the user's roles from the ProjectAccessRoleTable
        user_roles = self.request.user.projectaccessroletable_set.all()
        
        # Get the project ids associated with the user's roles
        project_ids = user_roles.values_list('project_access_table__project', flat=True)
        
        # Filter projects based on the user's roles
        projects = Project.objects.filter(id__in=project_ids).distinct()
        
        return projects
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AuthPermissions.IsHOD |  AuthPermissions.IsPGCoordinator | AuthPermissions.IsUGCoordinator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [ProjectPermission.UpdatePermission]
        elif self.action == 'destroy':
            permission_classes = [ProjectPermission.ProjectDeletePermission]
        elif self.action == 'retrieve':
            permission_classes = [ProjectPermission.ReadPermission]
        elif self.action == 'list':
            permission_classes = [ProjectPermission.ProjectListPermission]
        else:
            permission_classes = [AuthPermissions.IsHOD]
            
        return [permission() for permission in permission_classes]

class ProjectAccessTableViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectAccessTable.objects.all()
    serializer_class = ProjectAccessTableSerializer   
    permission_classes = [ProjectPermission.ListPermission]
    
    def get_queryset(self):
        queryset = ProjectAccessTable.objects.filter(project__pk=self.kwargs['project_pk'])
        return queryset
    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [ProjectPermission.ListPermission]
    #     else:
    #         permission_classes = [ProjectPermission.ReadPermission]
            
        return [permission() for permission in permission_classes]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if len(queryset) == 0:
            return Response({'detail':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProjectAccessRoleTableViewset(viewsets.ModelViewSet):
    queryset = ProjectAccessRoleTable.objects.all()
    serializer_class = ProjectAccessRoleTableSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_access_table'] = ProjectAccessTable.objects.filter(pk=self.kwargs['access_table_pk']).first()
        return context
    
    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [ProjectPermission.CreatePermission, ProjectPermission.UpdatePermission, ProjectPermission.DeletePermission]
        elif self.action == 'list':
            permission_classes = [ProjectPermission.ListPermission]
        elif self.action == 'retrieve':
            permission_classes = [ProjectPermission.ReadPermission]
            
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = ProjectAccessRoleTable.objects.filter(project_access_table__pk=self.kwargs['access_table_pk'], project_access_table__project__pk=self.kwargs['project_pk'])
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if len(queryset) == 0:
            return Response({'detail':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectTaskViewset(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    
    
    def get_queryset(self):
        queryset = ProjectTask.objects.filter(project__pk=self.kwargs['project_pk'])
        return queryset
        
    def get_serializer_context(self):
        project = Project.objects.filter(pk=self.kwargs['project_pk']).first()
        context = super().get_serializer_context()
        context['project'] = project
        return context
    
    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [ProjectPermission.CreatePermission, ProjectPermission.UpdatePermission, ProjectPermission.DeletePermission]
        elif self.action == 'list':
            permission_classes = [ProjectPermission.ListPermission]
        elif self.action == 'retreieve':
            permission_classes = [ProjectPermission.ReadPermission]
        else:
            permission_classes = [ProjectPermission.ReadPermission]
            
        return [permission() for permission in permission_classes]
    
class ProjectTaskCommentViewset(viewsets.ModelViewSet):
    queryset = ProjectTaskComment.objects.all()
    serializer_class = ProjectTaskCommentSerializer
    
    def get_queryset(self):
        queryset = ProjectTaskComment.objects.filter(task__pk=self.kwargs['task_pk'])
        return queryset
    
    def get_permissions(self):
        if self.action  == 'create':
            permission_classes = [ProjectPermission.CommentCreatePermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [ProjectPermission.CommentUpdatePermission]
            
        elif self.action in ['list', 'retrieve']:
            permission_classes = [ProjectPermission.CommentReadPermission]
        elif self.action == 'destroy':
            permission_classes = [ProjectPermission.CommentDeletePermission]
        else:
            permission_classes = [ProjectPermission.CommentReadPermission]
            
        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        project_task = ProjectTask.objects.filter(pk=self.kwargs['task_pk']).first()
        context['project_task'] = project_task
        context['commented_by'] = self.request.user
        return context
    
class ProjectTaskAssigneeViewset(viewsets.ModelViewSet):
    queryset = ProjectTaskAssignment.objects.all()
    serializer_class = ProjectTaskAssigneeSerializer
    permission_classes = (AuthPermissions.IsAuthenticated, )
    
    def get_queryset(self):
        queryset = ProjectTaskAssignment.objects.filter(task__pk=self.kwargs['task_pk'])
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        project_task = ProjectTask.objects.filter(pk=self.kwargs['task_pk']).first()
        context['project_task'] = project_task
        return context
    