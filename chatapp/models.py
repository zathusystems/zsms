from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
class Chat(models.Model):
    u=get_user_model()
    users=models.ManyToManyField(u, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    udated_at = models.DateTimeField(default=None, null=True, blank=True)
    show_onpage=models.BooleanField(default=True)
    
    def unseen_msgs(self):
        msgs=self.chat_messages.filter(seen=False)
        if msgs:
            return msgs.last()
        return None
    
    def unseen_count(self):
        msgs=self.chat_messages.filter(seen=False)
        return msgs.count()
    

class Message(models.Model):
    u=get_user_model()
    chat=models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='chat_messages')
    sender = models.ForeignKey(u, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(u, on_delete=models.CASCADE, related_name='received_messages')
    seen=models.BooleanField(default=False)
    show_onpage=models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'
    
class DateStamp(models.Model):
    date=models.DateField(auto_now_add=True)
    chat=models.ForeignKey(Chat, related_name='date_messages', on_delete=models.CASCADE, null=True, blank=True, default=None)
    messages=models.ManyToManyField(Message, related_name='date_messages')
