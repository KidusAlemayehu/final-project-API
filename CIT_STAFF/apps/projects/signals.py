from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import ProjectTaskAssignment

@receiver(post_save, sender=ProjectTaskAssignment)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notify.send(instance.task.project.owner, recipient= instance.assignee, verb='assigned you to a task')