from django.shortcuts import render
from rest_framework import viewsets
from apps.staff_auth import permission_handler as AuthPermissions
import apps.event_schedule.permissions as EventPermissions
from apps.staff_user.models import OfficeChoices, RoleChoices
from .serializers import *
from .models import *

# Create your views here.
class EventScheduleViewset(viewsets.ModelViewSet):
    serializer_class = EventScheduleSerializer
    queryset = EventSchedule.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['created_by'] = self.request.user
        return context
    
    def get_queryset(self):
        user = self.request.user
        if self.request.user.roles.filter(office__name=OfficeChoices.HOD, role=RoleChoices.ADMINISTRATOR).exists():
            queryset = EventSchedule.objects.all()
        elif self.request.user.roles.filter(office__name=OfficeChoices.UG, role=RoleChoices.HEAD).exists():
            queryset = EventSchedule.objects.all()
        elif self.request.user.roles.filter(office__name=OfficeChoices.PG, role=RoleChoices.COORDINATOR).exists():
            queryset = EventSchedule.objects.all()
        else:
            invitations = EventInvitation.objects.filter(invited=user)
            event_ids = invitations.values_list('event_schedule_id', flat=True)
            queryset =  EventSchedule.objects.filter(id__in=event_ids)
        return queryset
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
           permission_classes = [EventPermissions.EventUpdatePermission]
        elif self.action in ['list']:
           permission_classes = [AuthPermissions.IsAuthenticated]
        else:
            permission_classes = [AuthPermissions.IsHOD | AuthPermissions.IsPGCoordinator | AuthPermissions.IsUGSectionHead]
            
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