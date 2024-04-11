from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from apps.staff_auth import permission_handler as AuthPermissions
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

class ProjectAccessTableViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectAccessTable.objects.all()
    serializer_class = ProjectAccessTableSerializer    
    
    def get_queryset(self):
        queryset = ProjectAccessTable.objects.filter(project__pk=self.kwargs['project_pk'])
        return queryset
    
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
    