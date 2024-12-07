from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from assignments.models import Assignment, Submission
from attendance.models import StudentAttendanceStatus
from classroom.models import ClassRoom
from exams.models import Exam, Result
from finance.models import Fee, FeeCategory, OtherFee
from library.models import Checkout
from parent.models import ParentDetails, ParentStudentAccess
from school_calendar.models import AcademicYear, Term
from timetable.models import TimeTable
from .forms import *
from .models import Student, Subject
from django.http import JsonResponse
from main.utils import *
from datetime import datetime

# Create your views here.
# students viws
@login_required
def students(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    form=StudentForm()
    enform=EnrollmentForm()
    fee_categories=FeeCategory.objects.filter(school=institution)
    
    students=Student.objects.filter(school=institution)
    clases=ClassRoom.objects.filter(school=institution)
    cont={
        'students':students,
        'form':form,
        'form2':enform,
        'classes':clases,
        'fee_categories':fee_categories,
        'school_id':school_id,
        'institution':institution
    }
    if is_class_teacher(request):
        tch=get_instructor(request)
        clas=ClassRoom.objects.get(school=institution, teacher_assigned=tch)
        cont2={
            'students':clas.students.all(),
            'class':clas,
            'school_id':school_id,
            'institution':institution
        }
        return render(request, 'templates/classroom/single_class_students.html', cont2)
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    return render(request, 'templates/student/students.html', cont)


@login_required
def student_form(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    form=StudentForm()
    enform=EnrollmentForm()
    fee_categories=FeeCategory.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution).exclude(period='once off')
    if request.method=='POST':
        form=StudentForm(request.POST)
        enform=EnrollmentForm(request.POST)
        if form.is_valid() and enform.is_valid():
            cls_id=request.POST.get('class', '')
            cls=ClassRoom.objects.get(id=cls_id)
            student=form.save(commit=False)
            student.school=institution
            student.save()

            cls.students.add(student)

            enrollment=enform.save(commit=False)
            enrollment.student=student
            enrollment.school=institution
            enrollment.save()
            
            fee_id=request.POST.get('fee_category_id', '')
            fee_cate=FeeCategory.objects.get(id=fee_id)
            fee_cate.enrollment.add(enrollment)
            fee_cate.save()

            other_fee_ids=request.POST.getlist('other_fee_id', '')
            for other_fee_id in other_fee_ids:
                other_fee=OtherFee.objects.get(id=other_fee_id)
                other_fee.enrollment.add(enrollment)
                other_fee.save()

            subject_ids=request.POST.getlist('subjects', '')
            for subject_id in subject_ids:
                subject=Subject.objects.get(id=subject_id)
                enrollment.subjects.add(subject)
            enrollment.save()
    students=Student.objects.filter(school=institution)
    clases=ClassRoom.objects.filter(school=institution)
    cont={
        'students':students,
        'form':form,
        'form2':enform,
        'classes':clases,
        'fee_categories':fee_categories,
        'school_id':school_id,
        'institution':institution,
        'other_fees':other_fees
    }
    # if is_class_teacher(request):
    #     tch=get_instructor(request)
    #     clas=ClassRoom.objects.get(school=institution, teacher_assigned=tch)
    #     cont2={
    #         'students':clas.students.all(),
    #         'class':clas,
    #         'school_id':school_id,
    #         'institution':institution
    #     }
    #     return render(request, 'templates/classroom/single_class_students.html', cont2)
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    return render(request, 'templates/student/student_form.html', cont)


# single student views
@login_required
def single_student(request, stu_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    stu=get_object_or_404(Student, id=stu_id)
    enr=get_object_or_404(Enrollment, student=stu)
    print(enr.other_fees.all(), 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
    form=StudentForm(instance=stu)
    enform=EnrollmentForm(instance=enr)
    cate=FeeCategory.objects.get(enrollment=enr)
    fee=Fee.objects.filter(fee_category=cate).last()
    parent_d=ParentDetails.objects.filter(student=stu).first()
    parent=None
    access=ParentStudentAccess.objects.filter(student=stu, approved=True).first()
    if access:
        parent=access.parent

    if request.method=='POST':
        form=StudentForm(request.POST, instance=stu)
        enform=EnrollmentForm(request.POST, instance=enr)
        if form.is_valid() and enform.is_valid():
            form.save()
            enform.save()
    cont={
        'student':stu,
        'parent_d':parent_d,
        'parent':parent,
        'form':form,
        'form2':enform,
        'enrollment':enr,
        'fee_category':cate,
        'fee':fee,
        'school_id':school_id,
        'institution':institution,
        'is_admin':is_admin(request)
    }
    # if is_teacher(request):
    #     tch=get_instructor(request)
    #     clas=ClassRoom.objects.get(school=institution, teacher_assigned=tch)
    return render(request, 'templates/classroom/single_class_student.html', cont)
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    # return render(request, 'templates/student/student.html', cont)

def student_update(request, stu_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    stu=get_object_or_404(Student, id=stu_id)
    enr=get_object_or_404(Enrollment, student=stu)
    form=StudentForm(instance=stu)
    enform=EnrollmentForm(instance=enr)
    cate=FeeCategory.objects.get(enrollment=enr)
    fee=Fee.objects.filter(fee_category=cate).last()
    if request.method=='POST':
        form=StudentForm(request.POST, instance=stu)
        enform=EnrollmentForm(request.POST, instance=enr)
        if form.is_valid() and enform.is_valid():
            form.save()
            enform.save()
    cont={
        'student':stu,
        'form':form,
        'form2':enform,
        'enrollment':enr,
        'fee_category':cate,
        'fee':fee,
        'school_id':school_id,
        'institution':institution
    }
    
    return render(request, 'templates/student/student.html', cont)



def exam_result(request, student_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    stu=get_object_or_404(Student, id=student_id)
    examresult=Result.objects.filter(student=stu).order_by('-date')
    cont={
        'student':stu,
        'examresults':examresult,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/student/exam_result.html', cont)

   
def attendance(request, student_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    stu=get_object_or_404(Student, id=student_id)
    attendance=StudentAttendanceStatus.objects.filter(student=stu)
    cont={
        'student':stu,
        'attendance':attendance,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/student/attendance.html', cont)


def book_checkouts(request, student_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    c_outs=Checkout.objects.filter(student__id=student_id)
    stu=get_object_or_404(Student, id=student_id)
    cont={
        'checkouts':c_outs,
        'child':stu,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/student/boo_checkouts.html', cont)

def assignments(request, student_id, school_id):
    institution=get_institution(request, school_id)
    student=get_object_or_404(Student, id=student_id)
    institution=get_institution(request, school_id)
    assignments = Assignment.objects.filter(school=institution, classi=student.class_students.first())
    cont={
        'assignments':assignments,
        'institution':institution,
        'school_id':school_id,
        'student':student
    }
    return render(request, 'templates/student/assignments.html', cont)


def exams(request, student_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    exam_schedules=Exam.objects.filter(school=institution)
    # form = ExamForm()
    # classes=ClassRoom.objects.filter(school=institution)
    # exam_subjects=ExamSubjects.objects.filter(id=exam_subject_id)
    # if request.method == 'POST':
    #     form = ExamForm(request.POST)
    #     cla=request.POST.getlist('classes', '')
    #     if form.is_valid():
    #         d=form.save(commit=False)
    #         d.school=institution
    #         d.academic_year=academic_year
            
    #         d.term=term
    #         d.save() 
    #         for cla_id in cla:
    #             cls=ClassRoom.objects.get(id=cla_id)
    #             d.classes.add(cls)
    #         d.save()
    #         return redirect('exams:exam', d.id, school_id)      
        
    cont={
        'exam_schedules': exam_schedules,
        'academic_year':academic_year,
        'term':term,
        # 'form':form,
        'student_id':student_id,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/student/exams.html', cont)