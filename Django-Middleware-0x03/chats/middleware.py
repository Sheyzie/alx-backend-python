from datetime import datetime
from django.conf import settings
import os


base_dir = settings.BASE_DIR
filename = 'request.log'

def log_request(entry):
    with open(os.path.join(base_dir, filename), 'a') as f:
        f.write(entry)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        log = f"{datetime.now()} - User: {user} - Path: {request.path}" + "\n"

        # log into request.log
        log_request(log)

        response = self.get_response(request)

        return response