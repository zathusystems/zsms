from django.urls import path
from . import views

app_name='finance'

urlpatterns = [
    path('fees-categories-<uuid:school_id>/', views.fee_categories, name='fee_categories'),
    path('fees-categories/collection-<int:cate_id>-<uuid:school_id>/', views.fee_list, name='fee_list'),
    path('fees-<uuid:school_id>/', views.fee_list2, name='fee_list2'),
    
    path('fees-categories/collection-<int:cate_id>/payments<int:fee_id>-<uuid:school_id>/', views.fee_payments, name='fee_payments'),
    path('fees-categories/other-fee-payments<int:fee_id>-<uuid:school_id>/', views.other_fee_payments, name='other_fee_payments'),
    path('fees-categories/collection-<int:cate_id>/payments<int:fee_id>/add_payment-<uuid:school_id>/', views.add_payment, name='add_payment'),
    path('fees-categories/other-fee-payments/add-<int:fee_id>/add_payment-<uuid:school_id>/', views.add_other_payment, name='add_other_payment'),
    
    path('financial-reports-<uuid:school_id>/', views.finance_reports, name='financial_reports'),
    # path('fees/delete/<int:pk>/', views.fee_delete, name='fee_delete'),
    # path('payments/', views.payment_list, name='payment_list'),
    # path('payments/add/', views.payment_add, name='payment_add'),
    # path('payments/update/<int:pk>/', views.payment_update, name='payment_update'),
    # path('payments/delete/<int:pk>/', views.payment_delete, name='payment_delete'),
    
    # Payroll URLs
    path('payrolls/<uuid:school_id>/', views.payroll_list, name='payroll_list'),
    path('Advance-salary-payments-<uuid:school_id>/', views.advance_payroll_list, name='ad_payroll_list'),
    path('Advance-salary-payments/add-<uuid:school_id>/', views.advance_payroll_form, name='add_advance'),
    path('payrolls/add-<uuid:school_id>/', views.payroll_form, name='payroll_add'),
    # path('payrolls/update/<int:pk>/', views.payroll_update, name='payroll_update'),
    # path('payrolls/delete/<int:pk>/', views.payroll_delete, name='payroll_delete'),
    
    # Expense URLs
    path('expenses-income-<uuid:school_id>/', views.income_expense, name='income_expense'),
    path('invoicing-<uuid:school_id>/', views.invoicing, name='invoicing'),
    path('invoicing/invoice-add-<uuid:school_id>/', views.invoice_add, name='invoice_add'),
    path('invoicing/invoice-view-<int:inv_id>-<uuid:school_id>/', views.invoice_view, name='invoice_view'),
    # path('expenses/update/<int:pk>/', views.expense_update, name='expense_update'),
    # path('expenses/delete/<int:pk>/', views.expense_delete, name='expense_delete'),
]
