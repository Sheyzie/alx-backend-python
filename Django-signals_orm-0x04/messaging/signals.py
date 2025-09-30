from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Message
from .utils import log_to_message_history


@receiver(pre_save, sender=Message)
def save_message_history_on_update(sender, instance, **kwargs):
    if instance.id:
        try:
            message = Message.objects.get(id=instance.id)
            log_to_message_history(message)
        except Message.DoesNotExist:
            pass