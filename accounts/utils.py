# from django.utils import timezone
# from datetime import timedelta
# from django.shortcuts import get_object_or_404

# from accounts.models import CustomUser


# def is_user_online(user):
#     # Define an "online" threshold in minutes
#     online_threshold = timezone.now() - timedelta(minutes=5)
#     user_profile = get_object_or_404(CustomUser, id=user.id)
    
#     # Check if user's last seen is within the online threshold
#     return user_profile.last_seen >= online_threshold
