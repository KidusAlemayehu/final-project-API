from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from apps.staff_auth import permission_handler as AuthPermissions
from apps.staff_user.models import StaffUser

# Create your views here.
class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = (AuthPermissions.IsAuthenticated,)
    
    def get_serializer_context(self):
        user = StaffUser.objects.filter(pk=self.request.user.pk).first()
        context = super().get_serializer_context()
        context['owner'] = user
        return context

class ProjectAccessTableViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectAccessTable.objects.all()
    serializer_class = ProjectAccessTableSerializer    
    
    def get_queryset(self):
        queryset = ProjectAccessTable.objects.filter(project__pk=self.kwargs['project_pk'])
        return queryset
    
class ProjectAccessRoleTableViewset(viewsets.ModelViewSet):
    queryset = ProjectAccessRoleTable.objects.all()
    serializer_class = ProjectAccessRoleTableSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_access_table'] = ProjectAccessTable.objects.filter(pk=self.kwargs['access_table_pk']).first()
        return context

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
    