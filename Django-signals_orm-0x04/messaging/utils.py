from .models import Notification, MessageHistory



def create_message_notification(message):
    Notification.objects.create(message=message, receiver=message.receiver)

def log_to_message_history(message):
    if message.edited == True:
        message_history = MessageHistory.objects.create(message=message, message_body=message.message_body)