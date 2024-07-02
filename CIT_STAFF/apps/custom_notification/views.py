from django.shortcuts import render
from rest_framework import viewsets
from notifications.models import Notification
from .serializers import NotificationsSerializer
from apps.staff_auth import permission_handler as AuthPermissions
from apps.staff_user.models import OfficeChoices, RoleChoices

# Create your views here.
class UserNotificationsView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [AuthPermissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.roles.filter(office__name=OfficeChoices.HOD, role=RoleChoices.ADMINISTRATOR).exists():
            queryset = queryset
        else:
            queryset = queryset.filter(recipient=self.request.user.id)
        return queryset.order_by('-timestamp')
    