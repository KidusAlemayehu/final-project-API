from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import EventInvitation

@receiver(post_save, sender=EventInvitation)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notify.send(instance.invited_by, recipient=instance.invited, verb='invited you to an event')
        print('created')