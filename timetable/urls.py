from django.urls import path
from .views import *

app_name='timetable'
urlpatterns = [
    path('all-time-tables-<uuid:school_id>/', time_tables, name='time_tables'),
    path('time-table/<int:table_id>-<uuid:school_id>/', time_table, name='time_table'),
    path('class-time-table/<int:table_id>-<uuid:school_id>/', inclass_time_table, name='inclass_time_table'),
]
