from django.urls import path
from .views import *

app_name='student'
urlpatterns = [
    path('students-<uuid:school_id>/', students, name='students'),
    path('students/add-enroll-<uuid:school_id>/', student_form, name='student_form'),
    path('students/<int:stu_id>-<uuid:school_id>/', single_student, name='student'),
    path('students/update/<int:stu_id>-<uuid:school_id>/', student_update, name='update'),
    path('student/exams-<int:student_id>-<uuid:school_id>/', exams, name='exams'),
    path('student/exam-result-<int:student_id>-<uuid:school_id>/', exam_result, name='exam_result'),
    path('student/attendance-<int:student_id>-<uuid:school_id>/', attendance, name='atte'),
    path('student/assignments-<int:student_id>-<uuid:school_id>/', assignments, name='ass'),
    path('student/book-checkouts-<int:student_id>-<uuid:school_id>/', book_checkouts, name='check_outs')
]
