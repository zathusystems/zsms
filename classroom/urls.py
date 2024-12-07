from django.urls import path
from .views import *

app_name='class_room'
urlpatterns = [
    path('classes-<uuid:school_id>/', classes, name='classes'),
    path('classes/<int:class_id>-<uuid:school_id>/', class_detail, name='class_detail'),
    path('classes/<int:class_id>-<int:stu_id>-<uuid:school_id>/', add_student_class, name='add_class'),
    path('my-class-<uuid:school_id>/', instructor_class_detail, name='instructor_class_detail'),
    path('class-room/exam-subjects/<int:exam_id>-<int:class_id>-<uuid:school_id>/', class_exam_subjects, name='exam_subjects'),
]
