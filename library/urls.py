from django.urls import path
from . import views

app_name='library'
urlpatterns = [
    path('books-<uuid:school_id>/', views.books, name='book_list'),
    path('books/book-copies-<int:book_id>-<uuid:school_id>/', views.book_copies, name='book_copies'),
    path('books/book-copies-<int:book_id>/checkout-<int:copy_id>-<uuid:school_id>/', views.book_checkout, name='checkout'),
    path('book-checkouts-<uuid:school_id>/', views.checkouts, name='checkouts'),
    # path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
]
