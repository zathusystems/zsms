from django.contrib import admin
from.models import Exam, ExamSubjects, Result, ExamDate
# Register your models here.
admin.site.register(Exam)
admin.site.register(ExamSubjects)
admin.site.register(Result)
admin.site.register(ExamDate)