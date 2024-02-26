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
        
        if self.request.user.role == 'Administrator':
            queryset = queryset
        else:
            queryset = queryset.filter(pk=self.request.user).first()
            
        return queryset
        
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [Permissions.IsAdministrator]
            
        else:
            permission_classes = [Permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    