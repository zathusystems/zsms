from django.urls import path
from .views import *

app_name='attendance'
urlpatterns = [
    path('subjects/student-attendance-<int:s_id>-<int:c_id>-<uuid:school_id>/', mark_student_attendance, name='attendance'),
    path('student-attendance-list-<uuid:school_id>/', student_attendance_list, name='student_attendance_list'),
    path('student-attendance-list/<int:atte_id><int:clas_id><int:sub_id>-<uuid:school_id>/', student_subject_attendance_list, name='student_sub_attendance_list'),
]
