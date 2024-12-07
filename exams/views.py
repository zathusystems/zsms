from django.shortcuts import redirect, render
from .models import *
from.forms import ExamDateForm, ExamForm, ExamResultsForm, ExamSubjectsForm
from main.utils import get_institution, is_approved_account
from classroom.models import ClassRoom

from .models import ExamSubjects

# Create your views here.

def exams(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    exam_schedules=Exam.objects.filter(school=institution)
    form = ExamForm()
    classes=ClassRoom.objects.filter(school=institution)
    # exam_subjects=ExamSubjects.objects.filter(id=exam_subject_id)
    if request.method == 'POST':
        form = ExamForm(request.POST)
        cla=request.POST.getlist('classes', '')
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.academic_year=academic_year
            
            d.term=term
            d.save() 
            for cla_id in cla:
                cls=ClassRoom.objects.get(id=cla_id)
                d.classes.add(cls)
            d.save()
            return redirect('exams:exam', d.id, school_id)      
        
    cont={
        'exam_schedules': exam_schedules,
        'academic_year':academic_year,
        'term':term,
        'form':form,
        'classes':classes,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/exams.html', cont)

# def exam_add_subjects(request):
#     if is_approved_account(request)==False: return redirect('main:un_approved') 
#     institution=get_institution(request)
#     academic_year=AcademicYear.objects.get(institution=institution, closed=False)
#     term=Term.objects.get(institution=institution, closed=False)
#     exam_schedule=Exam.objects.get(id=exam_id)
#     exam_dates=ExamDate.objects.filter(exam=exam_schedule)
#     form = ExamSubjectsForm()
#     if request.method == 'POST':
#         form = ExamSubjectsForm(request.POST)
#         if form.is_valid():
#             d=form.save(commit=False)
#             d.exam=exam_schedule
#             d.save() 
               
#     cont={
#         'exam_dates': exam_dates,
#         'exam_schedule':exam_schedule,
#         'academic_year':academic_year,
#         'term':term,
#         'form':form
#         }
#     return render(request, 'templates/exams/exam.html', cont)

def exam(request, exam_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    exam_schedule=Exam.objects.get(id=exam_id)
    exam_dates=ExamDate.objects.filter(exam=exam_schedule)
    form = ExamDateForm()
    if request.method == 'POST':
        form = ExamDateForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.exam=exam_schedule
            d.school=institution
            d.save() 

    cont={
        'exam_dates': exam_dates,
        'exam_schedule':exam_schedule,
        'academic_year':academic_year,
        'term':term,
        'form':form,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/exam.html', cont)

def exam_class_timetable(request, examdate_id, exam_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    exam_schedule=Exam.objects.get(id=exam_id)
    exam_date=ExamDate.objects.get(id=examdate_id)
    form = ExamSubjectsForm()
    if request.method == 'POST':
        form = ExamSubjectsForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.exam_date=exam_date
            d.exam=exam_schedule
            d.save() 

    cont={
        'exam_date': exam_date,
        'exam_schedule':exam_schedule,
        'academic_year':academic_year,
        'term':term,
        'form':form,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/exam_class_timetable.html', cont)


def exam_results(request, exam_subject_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    
    students=Student.objects.filter(school=institution)
    exam_subject=ExamSubjects.objects.get(id=exam_subject_id)
    exam=exam_subject.exam_date.exam
    results=Result.objects.filter(subject=exam_subject)
    
    form = ExamResultsForm()
    if request.method == 'POST':
        form = ExamResultsForm(request.POST)
        if form.is_valid():
            student_id=request.POST.get('student', '')
            student=Student.objects.get(id=student_id)
            d=form.save(commit=False)
            d.school=institution
            d.student=student
            d.subject=exam_subject
            d.save()
    result_students=[]
    for result in results:
        result_students.append(result.student)
             
    cont={
        'students':students,
        'result_students':result_students,
        'exam': exam,
        'exam_subject':exam_subject,
        'results':results,
        'academic_year':academic_year,
        'term':term,
        'form':form,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/exam_result.html', cont)


def add_exam_result(request, exam_subject_id, exam_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    
    students=Student.objects.filter(school=institution)
    exam=Exam.objects.get(id=exam_id)
    exam_subject=ExamSubjects.objects.get(id=exam_subject_id)
    results=Result.objects.filter(subject=exam_subject)
    
    form = ExamResultsForm()
    if request.method == 'POST':
        form = ExamResultsForm(request.POST)
        if form.is_valid():
            student_id=request.POST.get('student', '')
            student=Student.objects.get(id=student_id)
            d=form.save(commit=False)
            d.school=institution
            d.student=student
            d.subject=exam_subject
            d.save()
            if 'add-onother' in request.POST:pass
            else:return redirect('../')
            
    result_students=[]
    for result in results:
        result_students.append(result.student)
             
    cont={
        'students':students,
        'result_students':result_students,
        'exam': exam,
        'exam_subject':exam_subject,
        'results':results,
        'academic_year':academic_year,
        'term':term,
        'form':form,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/add_result.html', cont)


def exam_subjects(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)

    exam_timetables=Exam.objects.filter(academic_year=academic_year)
    exam_subjects=ExamSubjects.objects.filter(exam_date__school=institution)  
    cont={
        'exam_timetables':exam_timetables,
        'exam_subjects': exam_subjects,
        'academic_year':academic_year,
        'term':term,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/exam_subjects.html', cont)

def gen_report_cards(request, class_id, exam_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    classi=ClassRoom.objects.get(id=class_id)
    exam_timetable=Exam.objects.get(id=exam_id)
    exam_subjects=ExamSubjects.objects.filter(exam_date__school=institution) 

    if not exam_timetable.report_cards.all():
        students=classi.students.all()
        for student in students: 
            card=ReportCard()
            card.academic_year=academic_year
            card.term=term
            card.exam=exam_timetable
            card.student=student
            card.school=institution
            card.save() 
    cont={
        'exam':exam_timetable,
        'exam_subjects': exam_subjects,
        'academic_year':academic_year,
        'term':term,
        'classi':classi,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/exams/report_card.html', cont)
