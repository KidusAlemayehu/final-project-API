from django.shortcuts import render
from rest_framework import viewsets
from apps.staff_auth import permission_handler as AuthPermissions
import apps.event_schedule.permissions as EventPermissions
from .serializers import *
from .models import *

# Create your views here.
class EventScheduleViewset(viewsets.ModelViewSet):
    serializer_class = EventScheduleSerializer
    permission_classes = (AuthPermissions.IsAuthenticated, )
    queryset = EventSchedule.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['created_by'] = self.request.user
        return context
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
           permission_classes = [EventPermissions.EventUpdatePermission]
        else:
            permission_classes = [AuthPermissions.IsAuthenticated, ]
            
        return [permission() for permission in permission_classes]
    
    
class EventScheduleInvitation(viewsets.ModelViewSet):
    serializer_class = EventScheduleInvitationSerializer
    queryset = EventInvitation.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        event = EventSchedule.objects.filter(pk=self.kwargs['event_schedule_pk']).first()
        context['event_schedule'] = event
        context['invited_by'] = event.created_by
        return context
    
    def get_permissions(self):
        if self.action == 'create':
           permission_classes = [EventPermissions.EventInvitationCreatorPermission]
        else:
            permission_classes = [AuthPermissions.IsAuthenticated, ]
            
        return [permission() for permission in permission_classes]