from django.urls import path
from .views import *

app_name='exams'
urlpatterns = [
    path('exam-schedules-<uuid:school_id>/', exams, name='exams'),
    path('exam-schedules/exam-subjects<int:exam_id>-<uuid:school_id>/', exam, name='exam'),
    path('exam-schedules/exam-sujects-<uuid:school_id>/', exam_subjects, name='exam_subjects'),
    path('exam-schedules/exam-sujects/exam-results-<int:exam_subject_id>-<uuid:school_id>/', exam_results, name='exam_results'),
    path('exam-schedules/exam-sujects/exam-results-<int:exam_subject_id>/add-exam-result<int:exam_id>-<uuid:school_id>/', add_exam_result, name='add_exam_results'),
    path('exam-schedules/exam-sujects/class-time-table-<int:examdate_id>-<int:exam_id>-<uuid:school_id>/', exam_class_timetable, name='exam_class_subjects'),
    path('genarate-report-cards-<int:class_id>-<int:exam_id>-<uuid:school_id>/', gen_report_cards, name='gen'),

]
