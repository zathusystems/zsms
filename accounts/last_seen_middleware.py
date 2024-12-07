# middleware/last_seen_middleware.py

from django.utils import timezone
from django.conf import settings
from .models import CustomUser

class LastSeenMiddleware:
    """
    Middleware to update last_seen field of the user profile on every request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Update the user's last_seen time
            CustomUser.objects.filter(id=request.user.id).update(last_seen=timezone.now())
        
        response = self.get_response(request)
        return response
