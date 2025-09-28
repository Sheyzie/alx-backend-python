from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict, deque
from datetime import datetime
from django.conf import settings
import os


base_dir = settings.BASE_DIR
filename = 'requests.log'
msg_by_ip = []

def log_request(entry):
    with open(os.path.join(base_dir, filename), 'a') as f:
        f.write(entry)

def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get("REMOTE_ADDR")
        
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
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now()
        if not current_time.hour >= 18 and not current_time.hour <= 21:
            return Response({'detail': 'chat cannot be outside 9PM and 6PM'}, status=status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)

        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.messages_sent = defaultdict(lambda: deque())
        self.limit = 5 # requests
        self.window = 60 # seconds

    def __call__(self, request):
        key = get_client_ip(request)
        now = datetime.now()
        q = self.messages_sent[key]

        while q and q[0] <= now - self.window:
            q.popleft()
        if len(q) >= self.limit:
            return Response({"error":"rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        q.append(now)
        return self.get_response(request)