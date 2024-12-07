"""
URL configuration for ZSMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('landing_page.urls')),
    path('student-attendance/', include('attendance.urls')),
    path('accounts/', include('accounts.urls')),
    path('teachers-mangement/', include('teacher.urls')),
    path('students-mangement/', include('student.urls')),
    path('class-mangement/', include('classroom.urls')),
    path('library/', include('library.urls')),
    path('timetable/', include('timetable.urls')),
    path('adminstration/', include('schooladminstration.urls')),
    path('employee-management/', include('employee.urls')),
    path('finance-management/', include('finance.urls')),
    path('exam-management/', include('exams.urls')),
    path('school-calendar/', include('school_calendar.urls')),
    path('', include('subscription.urls')),
    path('parent/', include('parent.urls')),
    path('', include('text_to_voice.urls')),
    path('chat', include('chatapp.urls')),
    path('', include('search.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
