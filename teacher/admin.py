from django.contrib import admin
from .models import *
from assignments.models import *
# Register your models here.
admin.site.register(Instructor)
admin.site.register(LessonPlan)

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(ClassWork)
admin.site.register(ClassWorkResult)
