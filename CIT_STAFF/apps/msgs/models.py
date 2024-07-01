from django.db import models
from apps.staff_user.models import StaffUser

# Create your models here.
class Message(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    body = models.TextField()
    sender = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = "Message"

def attachment_path(instance, filename):
    return 'Attachments/Messages/Message_{0}_to_{1}/{2}'.format(instance.message.sender, instance.message.receiver, filename)        
class MessageAttachment(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    attachment = models.FileField(upload_to=attachment_path)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Message_Attachment"