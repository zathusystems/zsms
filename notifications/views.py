from django.shortcuts import redirect, render
from schooladminstration.models import Institution as School
from main.utils import get_institution, is_admin, is_approved_account

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notice
from .forms import NoticeForm

# Display notice board for a specific audience
@login_required
def notice_board(request):
    user_group = 'All'
    if request.user.groups.filter(name='Teachers').exists():
        user_group = 'Teachers'
    elif request.user.groups.filter(name='Students').exists():
        user_group = 'Students'
    elif request.user.groups.filter(name='Parents').exists():
        user_group = 'Parents'
    
    notices = Notice.objects.filter(audience__in=[user_group, 'All'])
    return render(request, 'notices/notice_board.html', {'notices': notices})

# Create a new notice (for admins or staff)
@login_required
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()
            return redirect('notice_board')
    else:
        form = NoticeForm()
    return render(request, 'notices/create_notice.html', {'form': form})

# Update a notice
@login_required
def update_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_board')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'notices/update_notice.html', {'form': form})

# Delete a notice
@login_required
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    return redirect('notice_board')










from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserNotification, Notification

@login_required
def notifications_view(request, school_id):
    """Displays the list of notifications for the logged-in user."""
    notifications = Notification.objects.filter(recipient=request.user, school=)
    return render(request, 'templates/notifications/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """Marks a specific notification as read."""
    user_notification = get_object_or_404(UserNotification, id=notification_id, recipient=request.user)
    user_notification.mark_as_read()
    return redirect('notifications')

@login_required
def create_notification(request):
    """View to create a new notification (for school admins)."""
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        notification_type = request.POST['notification_type']
        school = School.objects.get(id=request.POST['school_id'])
        
        notification = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            school=school,
            sender=request.user
        )
        
        # Target all users related to the school (e.g., students, teachers, etc.)
        for user in school.user_set.all():
            UserNotification.objects.create(notification=notification, recipient=user)
        
        return redirect('notifications')
    else:
        return render(request, 'notifications/create_notification.html', {
            'schools': School.objects.all()
        })
