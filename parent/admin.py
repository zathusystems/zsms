from django.contrib import admin
from .models import Parent, ParentStudentAccess, ParentDetails
# Register your models here.

admin.site.register(Parent)
admin.site.register(ParentDetails)
admin.site.register(ParentStudentAccess)