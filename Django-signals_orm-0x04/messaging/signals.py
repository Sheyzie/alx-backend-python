from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q


from .models import Message, Notification, MessageHistory
# from .utils import create_message_notification, log_to_message_history


User = get_user_model()

def create_message_notification(message):
    Notification.objects.create(message=message, receiver=message.receiver)

def log_to_message_history(message):
    if message.edited == True:
        message_history = MessageHistory.objects.create(message=message, message_body=message.message_body, edited_by=message.sender)

def delete_user_entries(user):
    Message.objects.filter(Q(sender=user) | Q(receiver=user)).delete()
    Notification.objects.filter(receiver=user).delete()
    MessageHistory.objects.filter(edited_by=user).delete()



@receiver(post_save, sender=Message)
def create_notification_on_created_message(sender, instance, created, **kwargs):
    if created:
        create_message_notification(instance)

@receiver(pre_save, sender=Message)
def save_message_history_on_update(sender, instance, **kwargs):
    if instance.id:
        try:
            message = Message.objects.get(id=instance.id)
            log_to_message_history(message)
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def clean_up_on_user_delete(sender, instance, using, **kwargs):
    delete_user_entries(instance)