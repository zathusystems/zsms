from django.urls import path
from .views import *

app_name='main'
urlpatterns = [
    path('dashboard-<uuid:school_id>/', dashboard, name='dashboard'),
    path('my-profile-<uuid:school_id>/', MyProfile, name='profile'),
    path('account-waiting-approval-<uuid:school_id>/', un_approved, name='un_approved'),
    path('un-authorise-access-<uuid:school_id>/', un_authorised, name='un_authorised'),
    path('add-data/<slug:title>-<uuid:school_id>/', add_data, name='add_data'),
    path('notices-board-<uuid:school_id>/', notice_board, name='notice_board'),    
]
