from .models import Chat

def chat_global_data(request):
    chats=None
    if request.user.is_authenticated:
        chats=Chat.objects.filter(users=(request.user)).order_by('-udated_at')
        counter_chats=Chat.objects.filter(users=(request.user)).order_by('-udated_at')[:6]
        counter=0
        for chat in counter_chats:
            messages=chat.chat_messages.filter(receiver=request.user, seen=False)
            if messages:
                counter+=1
                continue
        return {'counter_chats':counter_chats, 'chats': chats, 'counter':counter}
    return {'mkkk': chats}