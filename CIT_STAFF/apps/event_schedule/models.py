from django.db import models
from apps.staff_user.models import StaffUser

# Create your models here.
class EventSchedule(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    subject = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    schedule_time = models.DateTimeField()
    created_by = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = "Event_Schedule"
    
class EventInvitation(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    event_schedule = models.ForeignKey(EventSchedule, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, related_name='invited_by')
    invited = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, related_name='invited')
    
    class Meta:
        db_table = "Event_Invitation"