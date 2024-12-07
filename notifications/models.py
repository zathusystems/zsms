from django.db import models

from schooladminstration.models import Institution

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

class Notice(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='notices')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posted_notices", default=None)
    audience = models.CharField(max_length=100, choices=[('all', 'All'), ('teachers', 'Teachers'), ('students', 'Students'), ('parents', 'Parents')])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('announcement', 'Announcement'),
        ('assignment', 'Assignment'),
        ('fee_reminder', 'Fee Reminder'),
        ('event', 'Event'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    show_onpage = models.BooleanField(default=True)
    i_d=models.IntegerField(max_length=10, default=None, blank=True, null=True)
    is_user_notif = models.BooleanField(default=False, blank=True, null=True)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications', default=None, blank=True, null=True)
    def __str__(self):
        return f"{self.title} - {self.school.institution_name}"

    class Meta:
        ordering = ['-created_at']


class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), related_name='received_notifications', on_delete=models.CASCADE, default=None)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.recipient.first_name} {self.recipient.last_name}: {self.notification.title}"

    class Meta:
        ordering = ['-created_at']