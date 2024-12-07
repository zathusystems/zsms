from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from student.models import Enrollment
from timetable.models import TimeTable
from .forms import *
from .models import Student, Subject
from django.http import JsonResponse
from main.utils import *
from .models import StudentAttendanceStatus
from datetime import datetime

@login_required
def student_attendance_list(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    print(institution)
    attendance=StudentAttendance.objects.filter(school=institution)
    class_rooms=ClassRoom.objects.filter(school=institution)
    time_table_data=TimeTable.objects.filter(school=institution)
    cont={
        'data':time_table_data,
        'attendance_list':attendance,
        'class_rooms':class_rooms,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/attendance/class_attedance.html', cont)

@login_required
def student_subject_attendance_list(request, atte_id, clas_id, sub_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    print(institution)
    attendance=StudentAttendance.objects.get(school=institution, id=atte_id)
    class_room=ClassRoom.objects.get(id=clas_id)
    subject=Subject.objects.get(id=sub_id)
    # time_table_data=TimeTable.objects.filter(school=institution)
    cont={
        'subject':subject,
        'attendance':attendance,
        'class_room':class_room,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/attendance/class_subject_attedance.html', cont)

# students attendants views
@login_required
def mark_student_attendance(request, s_id, c_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    subject=Subject.objects.get(id=s_id)
    print(subject.enrollement.all(), 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')

    students=Student.objects.filter(enrollement__subjects=subject, school=institution)
    enr=Enrollment.objects.filter(subjects=subject)
    print(students, enr, 'llllllllllllllllllllllllllllllllllll')
    clas=ClassRoom.objects.get(school=institution, id=c_id)
    form=StudentAttendanceForm()
    print(datetime.today())
    attendance=StudentAttendance.objects.filter(subject=subject)

    print(attendance)
    already_marked=False
    for atte in attendance:
        print(atte.date.date(), datetime.today().date())
        if atte.date.date()==datetime.today().date() and atte.class_room==clas:
            already_marked=True
            print('match')
            continue
        else:
            pass

    if request.method=='POST':
        statuses=request.POST.getlist('status')
        students_ids=request.POST.getlist('student')
        print(statuses, students_ids)
        s_atendance=StudentAttendance.objects.create(subject=subject, class_room=clas, school=institution)
        s_atendance.save()
        i=0
        for student_id in students_ids:
            status=statuses[i]
            print(status)
            student=Student.objects.get(id=student_id)
            StudentAttendanceStatus.objects.create(status=status, attendance=s_atendance, student=student)
            i+=1
        return redirect('timetable:time_tables', school_id)
    
    form=StudentAttendanceForm()
    cont={
        'students':students,
        'subject':subject,
        'form':form,
        'clas':clas,
        'already_marked':already_marked,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/attendance/mark_attendance.html', cont)
