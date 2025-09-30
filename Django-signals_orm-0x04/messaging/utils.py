from .models import MessageHistory


def log_to_message_history(message):
    if message.edited == True:
        message_history = MessageHistory.objects.create(message=message, message_body=message.message_body)