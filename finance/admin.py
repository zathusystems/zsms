from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Payroll)
admin.site.register(AdvancePayroll)
admin.site.register(FeeCategory)
admin.site.register(FeePayment)
admin.site.register(Fee)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(PayrollReconciliation)
admin.site.register(OtherFee)

