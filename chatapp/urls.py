# messaging/urls.py

from django.urls import path
from . import views
app_name='chat'
urlpatterns = [
    path('chats/inbox-<int:user_id>-<int:chat_id>/', views.inbox, name='inbox'),
    path('initiate/<int:user_id>/', views.initiate, name='init'),
    path('chats/', views.chat, name='chat'),

    path('chats/inbox-<int:user_id>-<int:chat_id>-<uuid:school_id>/', views.inbox2, name='inbox2'),
    path('initiate/<int:user_id>-<uuid:school_id>/', views.initiate2, name='init2'),
    path('chats-<uuid:school_id>/', views.chat2, name='chat2'),
]
