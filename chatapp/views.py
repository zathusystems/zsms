# messaging/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.models import CustomUser
from main.utils import get_institution
from .models import DateStamp, Message, Chat
from .forms import MessageForm

@login_required
def initiate(request, user_id):
    reciever=CustomUser.objects.get(id=user_id)
    try:
        # chat=Chat.objects.get(users=(reciever.id and request.user.id))
        chat = Chat.objects.filter(
            users=reciever.id
        ).get(
            users=request.user.id
        )
    except:
        chat=Chat()
        chat.save()
        chat.users.add(reciever, request.user)
    return redirect('chat:inbox', user_id, chat.id)

@login_required
def inbox(request, user_id, chat_id):
    reciever=CustomUser.objects.get(id=user_id)
    chat=Chat.objects.get(id=chat_id)
    if request.method == 'POST':
        content=request.POST.get('content')
        m=Message()
        m.receiver=reciever
        m.sender=request.user
        m.content=content
        m.chat=chat
        m.save()
        chat.udated_at=timezone.now()
        chat.save()
        try:
            datestamp=DateStamp.objects.get(date=m.timestamp.date(), chat=chat)
            datestamp.chat=chat
            datestamp.save()
            datestamp.messages.add(m)
            # print(m.timestamp.date(), datestamp.date, chat.created_at.date(), 'kkkkkkkkkkkkkkkkkkkkkkk')
        except:
            datestamp=DateStamp()
            datestamp.chat=chat
            datestamp.save()
            datestamp.messages.add(m)
    messages = chat.chat_messages.all().order_by('timestamp')
    datestaps=DateStamp.objects.filter(chat=chat)
    for ms in messages.filter(seen=False, receiver=request.user):
        ms.seen=True
        ms.save()
    # print(chat.id, messages, 'lllllllllllllllllllllllll')
    chats=Chat.objects.filter(users=request.user).order_by('-udated_at')
    cont={
        'datestamps':datestaps,
        'messages': messages,
        'chats':chats,
        'chat':chat
        }
    return render(request, 'templates/chatapp/inbox.html', cont)

@login_required
def chat(request):
    chats=Chat.objects.filter(users=request.user).order_by('-udated_at')
    cont={
        'chats': chats,
        }
    return render(request, 'templates/chatapp/chat.html', cont)



#chta view for school admins 
@login_required
def initiate2(request, user_id, school_id):
    reciever=CustomUser.objects.get(id=user_id)
    try:
        # chat=Chat.objects.get(users=(reciever.id and request.user.id))
        chat = Chat.objects.filter(
            users=reciever.id
        ).get(
            users=request.user.id
        )
    except:
        chat=Chat()
        chat.save()
        chat.users.add(reciever, request.user)
    return redirect('chat:inbox2', user_id, chat.id, school_id)

@login_required
def inbox2(request, user_id, chat_id, school_id):
    reciever=CustomUser.objects.get(id=user_id)
    chat=Chat.objects.get(id=chat_id)
    institution=get_institution(request, school_id)
    if request.method == 'POST':
        content=request.POST.get('content')
        m=Message()
        m.receiver=reciever
        m.sender=request.user
        m.content=content
        m.chat=chat
        m.save()
        chat.udated_at=timezone.now()
        chat.save()
        try:
            datestamp=DateStamp.objects.get(date=m.timestamp.date(), chat=chat)
            datestamp.chat=chat
            datestamp.save()
            datestamp.messages.add(m)
            # print(m.timestamp.date(), datestamp.date, chat.created_at.date(), 'kkkkkkkkkkkkkkkkkkkkkkk')
        except:
            datestamp=DateStamp()
            datestamp.chat=chat
            datestamp.save()
            datestamp.messages.add(m)
    messages = chat.chat_messages.all().order_by('timestamp')
    datestaps=DateStamp.objects.filter(chat=chat)
    for ms in messages.filter(seen=False, receiver=request.user):
        ms.seen=True
        ms.save()
    # print(chat.id, messages, 'lllllllllllllllllllllllll')
    chats=Chat.objects.filter(users=request.user).order_by('-udated_at')
    cont={
        'datestamps':datestaps,
        'messages': messages,
        'chats':chats,
        'chat':chat,
        'school_id':school_id,
        'institution':institution

        }
    return render(request, 'templates/chatapp/inbox2.html', cont)

@login_required
def chat2(request, school_id):
    chats=Chat.objects.filter(users=request.user).order_by('-udated_at')
    institution=get_institution(request, school_id)
   
    cont={
        'chats': chats,
        'school_id':school_id,
        'institution':institution,
        'hide_msgs':True
        }
    return render(request, 'templates/chatapp/chat2.html', cont)

