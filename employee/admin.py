from django.contrib import admin
from .models import Employee, EmployeeAttendance, LeaveRequest
# Register your models here.
admin.site.register(Employee)
admin.site.register(EmployeeAttendance)
admin.site.register(LeaveRequest)