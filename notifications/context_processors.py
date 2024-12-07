from .models import Notification

def notif_global_data(request):
    notifs=None
    if request.user.is_authenticated:

        notifs=Notification.objects.filter(recipient=request.user).order_by('-created_at')
        counter_notifs=Notification.objects.filter(recipient=request.user).order_by('-created_at')
        counter=0
        for notif in counter_notifs:
            # messages=notif.chat_messages.filter(receiver=request.user, seen=False)
            if notif.show_onpage:
                counter+=1
        return {'counter_notifs':counter_notifs, 'notifs': notifs, 'n_counter':counter}
    return {'mkkk': notifs}