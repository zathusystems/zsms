from django.urls import path
from .views import *

app_name='parent'
urlpatterns = [
    path('select-your-child', search_id, name='search_id'),
    path('parent-dashboard', dashboard, name='dash'),
    path('my-children', children, name='children'),
    path('schools', schools, name='schools'),
    path('schools/details-<uuid:school_id>/', school_info, name='school_info'),
    path('my-children/child-info-<int:student_id>/', child_info, name='child_info'),
    path('my-children/child-info/exam-result-<int:student_id>/', exam_result, name='exam_result'),
    path('my-children/child-info/attendance-<int:student_id>/', attendance, name='atte'),
    path('my-children/child-info/book-checkouts-<int:student_id>/', book_checkouts, name='check_outs'),
    path('my-children/child-info/assignments-<int:student_id>/', assignments, name='ass'),
    path('invoices/', invoices, name='invoices'),
    path('bacome-parent/', become_parent, name='become_parent'),
    path('invoices/invoice-view-<int:inv_id>/', invoice_view, name='invoice_view'),
    path('my-profile/', MyProfile, name='profile'),

]

