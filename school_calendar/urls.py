from django.urls import path
from .views import *

app_name='school_calendar'
urlpatterns = [
    path('calendar-list-<uuid:school_id>/', academic_calendar, name='calendar_list'),
    path('calendar-list/detail-<int:calendar_id>-<uuid:school_id>/', calendar_detail, name='calendar_detail'),
    path('events<uuid:school_id>/', events, name='events'),
    path('events/event-detail<int:event_id><uuid:school_id>/', event_detail, name='event_detail'),
]
