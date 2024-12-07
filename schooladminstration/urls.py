from django.urls import path
from .views import *

app_name='school_admin'
urlpatterns = [
    path('school-details-<uuid:school_id>/', school_info, name='school_info'),
    path('departments-<uuid:school_id>/', departments, name='departments'),
    path('department/<int:d_id>-<uuid:school_id>/', department, name='department'),
    path('parents/parent-view-<int:parent_id>-<uuid:school_id>/', parent, name='parent'),
    path('parents/<uuid:school_id>/', parents, name='parents'),
    path('staff-members/<uuid:school_id>/', Staff, name='staff'),
    path('add_parent_details/<uuid:school_id>-<int:student_id>/', add_parent_details, name='add_parent_details'),
]
