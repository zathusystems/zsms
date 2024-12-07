from django.urls import path
from .views import *


app_name='teacher'
urlpatterns = [
    # teachers urls
    path('teachers-<uuid:school_id>/', teachers, name='teachers'),
    path('teacher-requests-<uuid:school_id>/', teacher_requests, name='teacher_requests'),
    path('teachers/teacher-<int:t_id>-<uuid:school_id>/', single_teacher, name='teacher'),
    path('lesson-plan-list-<uuid:school_id>/', lesson_plan_list, name='lesson_plan_list'),
    path('lesson-plan-list/<int:pk>-<uuid:school_id>/', lesson_plan_detail, name='lesson_plan_detail'),
    path('lesson-plan-list/new/', lesson_plan_create, name='lesson_plan_create'),
    path('lesson-plan-list/<int:pk>/edit-<uuid:school_id>/', lesson_plan_update, name='lesson_plan_update'),
    path('lesson-plan-list/<int:pk>/delete-<uuid:school_id>/', lesson_plan_delete, name='lesson_plan_delete'),

    path('assignments/<int:pk>/submit-<uuid:school_id>/', submission_create, name='submission_create'),
    path('gradebook-<uuid:school_id>/', gradebook_list, name='gradebook_list'),
    path('gradebook/<int:pk>-<uuid:school_id>/', gradebook_detail, name='gradebook_detail'),
    
    path('assignments-<uuid:school_id>/', assignments, name='ass'),
    path('assignments/results-<int:pk>-<uuid:school_id>/', assignment_results, name='ass_results'),
    path('assignments/results/add-<int:pk>-<uuid:school_id>/', add_assignment_result, name='add_ass_results'),
    path('class-work-<uuid:school_id>/', class_works, name='work'),
    path('class-work/results-<int:pk>-<uuid:school_id>/', class_work_result, name='work_results'),
    path('class-work/results/add-<int:pk>-<uuid:school_id>/', add_class_work_result, name='add_work_results'),
    # path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-retrieve-update-destroy'),
]
