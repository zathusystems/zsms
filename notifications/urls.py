from django.urls import path
from . import views
app_name='notifications'
urlpatterns = [
    path('notices-<uuid:school_id>//', views.notice_board, name='notice_board'),
    path('notices/create/', views.create_notice, name='create_notice'),
    path('notices/update/<int:notice_id>/', views.update_notice, name='update_notice'),
    path('notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),
]



urlpatterns = [
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/create/', views.create_notification, name='create_notification'),
    path('notifications/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
]
