from rest_framework.permissions import BasePermission
from .models import EventSchedule

class EventInvitationCreatorPermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a create action!"
    
    def has_permission(self, request, view):
        event = view.kwargs.get("event_schedule_pk")
        event_obj = EventSchedule.objects.get(pk=event)
        if request.user == event_obj.created_by:
            return True
        return False
    
class EventUpdatePermission(BasePermission):
    message = "Permission Denied: You are not allowed to perform a update action!"
    
    def has_permission(self, request, view):
        event = view.get_object()
        if request.user == event.created_by or request.user.office == "HOD":
            return True
        else:
            return False