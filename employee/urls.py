from django.urls import path
from . import views

app_name='employee'
urlpatterns = [
    path('employees-<uuid:school_id>/', views.employee_list, name='employee_list'),
    path('employees/profile-<int:employee_id>-<uuid:school_id>/', views.employee_profile, name='employee_profile'),
    path('salary_reconciliations-<uuid:school_id>/', views.payroll_reconciliation, name='reco'),
    path('salary_reconciliations/form-<uuid:school_id>', views.reconciliation_form, name='reco_form'),
    path('leave-list-<uuid:school_id>/', views.leave_list, name='leave'),
    path('leave-list/add-<uuid:school_id>/', views.leave_add, name='leave_add'),
    path('employees/profile-<int:employee_id>/update-<uuid:school_id>/', views.employee_update, name='employee_update'),
    path('dates-of-attendance-<uuid:school_id>/', views.employee_attendance_dates, name='employee_attendance_dates'),
    path('dates-of-attendance/mark-attendance-<int:att_id>-<uuid:school_id>/', views.mark_employee_attendance, name='mark_attendance'),
    path('dates-of-attendance/attendance-list-<int:att_id>-<uuid:school_id>/', views.attendance_list, name='attendance_list'),
    path('delete/<int:pk>-<uuid:school_id>/', views.employee_delete, name='employee_delete'),
]

# from django.urls import path
# from .views import EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView

# urlpatterns = [
#     path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
#     path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-detail'),
# ]
