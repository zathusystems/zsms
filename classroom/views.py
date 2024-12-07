from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from assignments.models import Assignment
from attendance.models import StudentAttendance
from exams.models import Exam, ExamSubjects
from school_calendar.models import AcademicYear, Term
from timetable.models import TimeTable
from .forms import *
from .models import Student
from django.http import JsonResponse
from main.utils import *
from datetime import datetime


# view all institution classes
@login_required
def classes(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    classes=ClassRoom.objects.filter(school=institution)
    form=ClassForm()
    print(form.errors)
    teachers=Instructor.objects.filter(school_id=institution.id)
    if request.method=='POST':
        form=ClassForm(request.POST)
        teacher_id=request.POST.get('t_id')
        teacher=Instructor.objects.get(id=teacher_id)
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            t=d.teacher_assigned
            if t.assigned_class.all():
                msg='teacher is already assigned to onother class'
            else:
                d.teacher_assigned=teacher
                d.save()
            
        else:
            print(form.errors)
    cont={
        'teachers':teachers,
        'data':classes,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/classroom/classesi.html', cont)

# view class details
@login_required
def class_detail(request, class_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    classi=get_object_or_404(ClassRoom, id=class_id)
    stdnts=classi.students.all()
    attendance_list=StudentAttendance.objects.filter(class_room=classi)
    form=ClassForm2(instance=classi)
    assignments=Assignment.objects.filter(classi=classi).order_by('-created_at')
    exams=Exam.objects.filter(classes=classi)

    if request.method=='POST':
        form=ClassForm2(request.POST, instance=classi)
        if form.is_valid():
            form.save()
        
    cont={
        'assignments':assignments,
        'class':classi,
        'form':form,
        'students':stdnts,
        'attendance_list':attendance_list,
        'school_id':school_id,
        'institution':institution,
        'exams':exams
        
    }
    return render(request, 'templates/classroom/class_detail.html', cont)

# add new student to class
@login_required
def add_student_class(request, class_id, stu_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    classi=get_object_or_404(ClassRoom, id=class_id)
    stdnt=Student.objects.get(id=stu_id)
    classi.students.add(stdnt)
    classi.save()
    return redirect('class_room:class_detail', classi.id, school_id)

# view class details
@login_required
def instructor_class_detail(request, school_id):
    institution=get_institution(request, school_id)
    teacher=get_instructor(request)
    classi=None
    try:
        classi=get_object_or_404(ClassRoom, teacher_assigned=teacher)
    except:
        return render(request, 'templates/main/un_usigned.html')
    stdnts=classi.students.all()
    attendance_list=StudentAttendance.objects.filter(class_room=classi)

    day_of_week=datetime.today().weekday()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = days[day_of_week]

    cont={
        'class':classi,
        'today':day,
        'students':stdnts,
        'attendance_list':attendance_list,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/classroom/instructor_class.html', cont)


def class_exam_subjects(request, exam_id, class_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    classi=get_object_or_404(ClassRoom, id=class_id)
    exam_timetable=Exam.objects.get(id=exam_id)
    exam_subjects=ExamSubjects.objects.filter(exam=exam_timetable)  
    cont={
        'exam_subjects': exam_subjects,
        'exam_timetable': exam_timetable,
        'academic_year':academic_year,
        'term':term,
        'class':classi,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/classroom/exam_subjects.html', cont)

