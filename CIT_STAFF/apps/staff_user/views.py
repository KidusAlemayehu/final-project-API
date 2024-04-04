from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from apps.staff_auth import permission_handler as Permissions

# Create your views here.
class StaffUserViewset(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.office == 'HOD':
            queryset = queryset
        elif self.request.user.office == 'UG' and self.request.user.role == 'Coordinator':
            queryset = queryset.filter(office="UG")
        elif self.request.user.office == 'PG' and self.request.user.role == 'Coordinator':
            queryset = queryset.filter(office="PG")
        elif self.request.user.office == 'TA' and self.request.user.role == 'Coordinator':
            queryset = queryset.filter(office="TA")    
        else:
            queryset = queryset.filter(pk=self.request.user).first()
        filter = {}  
        try:
            office = self.request.GET.get('office')
        except:
            office = None
            
        try:
            role = self.request.GET.get('role')
        except:
            role = None

        if office:
            filter['office'] = office
        if role:
            filter['role'] = role
        queryset = queryset.filter(**filter)
        return queryset
        
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [Permissions.IsHOD | permissions.AllowAny]
        else:
            permission_classes = [Permissions.IsAuthenticated] 
        return [permission() for permission in permission_classes]
    
    