from rest_framework import serializers
from .models import *



class EventScheduleInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInvitation
        fields = ('id', 'event_schedule', 'invited_by', 'invited', 'created_at', 'updated_at')
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        attrs['event_schedule'] = self.context.get('event_schedule')
        attrs['invited_by'] = self.context.get('invited_by')
        return attrs
        
class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        fields = ('id', 'subject', 'description', 'schedule_time', 'created_by', 'link', 'created_at', 'updated_at')
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        
    def validate(self, attrs):
       attrs['created_by'] = self.context.get('created_by') 
       return attrs
   