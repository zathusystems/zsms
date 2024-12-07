from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from attendance.models import StudentAttendance
from classroom.models import ClassRoom
from employee.models import Employee
from notifications.utils import create_notif
from staff_permision.forms import PermisionForm
from staff_permision.models import Permision
from timetable.models import TimeTable
from .forms import *
from .models import *
from django.http import JsonResponse
from main.utils import *
from datetime import datetime


# from rest_framework import generics
# from .serializers import ItemSerializer

# class ItemListCreateView(generics.ListCreateAPIView):
#     queryset = Instructor.objects.all()
#     serializer_class = ItemSerializer

# class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Instructor.objects.all()
#     serializer_class = ItemSerializer






# Create your views here.
# teachers views
@login_required
def teachers(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    form=InstructorForm()
    if request.method=='POST':
        form=InstructorForm(request.POST)
        if form.is_valid():
            teacher=form.save(commit=False)
            teacher.school=institution
            teacher.save()

    teachers=Instructor.objects.filter(school=institution, approved=True)
    cont={
        'teachers':teachers,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/teacher/teachers.html', cont)

@login_required
def teacher_requests(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    # form=InstructorForm()
    teachers=Instructor.objects.filter(school=institution, approved=False)
    cont={
        'teachers':teachers,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/teacher/teacher_requests.html', cont)

# single teacher view
@login_required
def single_teacher(request, t_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    teacher=get_object_or_404(Instructor, id=t_id)
    form=InstructorForm(instance=teacher)
    permision_form=PermisionForm()
    pe=None
    try:
        pe=Permision.objects.get(user=teacher.user)
        permision_form=PermisionForm(instance=pe)
    except:pass
 
    if request.method=='POST':
        form=InstructorForm(request.POST, instance=teacher)
        permision_form=PermisionForm(request.POST)
        
        if pe:
            permision_form=PermisionForm(request.POST, instance=pe)
        
        if form.is_valid() and permision_form.is_valid():
            dd=form.save()
            if dd.approved:
                print('1 k;;;;;;;;;;;;;;k;;;;;;;;;')
                if teacher.employee.all():
                    print('2 ;kkkkkkkkkkkkkkkkkkkkkkk')
                    pass
                
                else:
                    print('3 ;kkkkkkkkkkkkkkkkkk')
                    Employee.objects.create(
                        school=institution,
                        teacher=teacher,
                        first_name=dd.first_name,
                        last_name=dd.last_name,
                        gender=dd.gender,
                        phone=dd.phone,
                        position=dd.role
                    )
                    create_notif(
                        'request approved', 
                        f'You can now access and manage {institution.institution_name}',
                        dd.user,
                        institution,
                        dd.user.id,
                        True
                    )
            if pe:
                d=permision_form.save(commit=False)
                d.save()
            else:
                d=permision_form.save(commit=False)
                d.school=institution
                d.user=teacher.user
                d.save()

    
    
        
    cont={
        'teacher':teacher,
        'permision_form':permision_form,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/teacher/teacher.html', cont)


@login_required
def lesson_plan_list(request, school_id):
    institution=get_institution(request, school_id)
    teacher=Instructor.objects.get(user=request.user)
    form = LessonPlanForm()
    print('1')
    if request.method == 'POST':
        print('2')
        form = LessonPlanForm(request.POST)
        if form.is_valid():
            print('3')
            lesson_plan = form.save(commit=False)
            lesson_plan.teacher = teacher
            lesson_plan.school=institution
            lesson_plan.save()
     
    else:
        form = LessonPlanForm()
    lesson_plans = LessonPlan.objects.filter(teacher=teacher).order_by('-date')
    cont={
        'lesson_plans':lesson_plans,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/teacher/lesson_plan_list.html', cont)

@login_required
def lesson_plan_detail(request, pk, school_id):
    institution=get_institution(request, school_id)
    teacher=Instructor.objects.get(user=request.user)
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    form = LessonPlanForm(instance=lesson_plan)
    if request.method == 'POST':
        print('2')
        form = LessonPlanForm(request.POST, instance=lesson_plan)
        if form.is_valid():
            form.save(commit=False)
    cont={
        'form':form,
        'lesson_plan':lesson_plan,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/teacher/lesson_plan_detail.html', cont)






@login_required
def lesson_plan_create(request):
    if request.method == 'POST':
        form = LessonPlanForm(request.POST)
        if form.is_valid():
            lesson_plan = form.save(commit=False)
            lesson_plan.teacher = request.user
            lesson_plan.save()
            return redirect('lesson_plan_list')
    else:
        form = LessonPlanForm()
    return render(request, 'lesson_planning/lesson_plan_form.html', {'form': form})

@login_required
def lesson_plan_update(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    if request.method == 'POST':
        form = LessonPlanForm(request.POST, instance=lesson_plan)
        if form.is_valid():
            form.save()
            return redirect('lesson_plan_detail', pk=pk)
    else:
        form = LessonPlanForm(instance=lesson_plan)
    return render(request, 'lesson_planning/lesson_plan_form.html', {'form': form})

@login_required
def lesson_plan_delete(request, pk):
    lesson_plan = get_object_or_404(LessonPlan, pk=pk)
    if request.method == 'POST':
        lesson_plan.delete()
        return redirect('lesson_plan_list')
    return render(request, 'lesson_planning/lesson_plan_confirm_delete.html', {'lesson_plan': lesson_plan})



def assignments(request, school_id):
    institution=get_institution(request, school_id)
    teacher=Instructor.objects.get(user=request.user)
    assignments = Assignment.objects.filter(school=institution).order_by('-created_at')
    form = AssignmentForm()
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            ass = form.save(commit=False)
            ass.teacher = teacher
            ass.school = institution
            ass.save()
        
    cont={
        'assignments':assignments,
        'institution':institution,
        'school_id':school_id,
        'form':form
    }
    return render(request, 'templates/teacher/assignments.html', cont)

def assignment_results(request, pk, school_id):
    institution=get_institution(request, school_id)
    teacher=Instructor.objects.get(user=request.user)
    institution=get_institution(request, school_id)
    assignment = get_object_or_404(Assignment, pk=pk)
 
    cont={
        'assignment':assignment,
        'institution':institution,
        'school_id':school_id,
        # 'form':form
    }
    return render(request, 'templates/teacher/ass_results.html', cont)


def add_assignment_result(request, pk, school_id):
    institution=get_institution(request, school_id)
    assignment = get_object_or_404(Assignment, pk=pk)
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            ass = form.save(commit=False)
            ass.assignment = assignment            
            ass.save()
    cont={
        'assignment':assignment,
        'institution':institution,
        'school_id':school_id,
        'form':form
    }
    return render(request, 'templates/teacher/ass_result_form.html', cont)



def class_works(request, school_id):
    institution=get_institution(request, school_id)
    teacher=Instructor.objects.get(user=request.user)
    works = ClassWork.objects.filter(school=institution).order_by('-date')
    form = ClassWorkForm()
    if request.method == 'POST':
        form = ClassWorkForm(request.POST)
        if form.is_valid():
            ass = form.save(commit=False)
            ass.teacher = teacher
            ass.school = institution
            # ass.student = request.user.studentprofile  # Assuming user is a student
            ass.save()
            # Update gradebook
            # gradebook, created = Gradebook.objects.get_or_create(student=submission.student, course=assignment.course)
            # gradebook.update_average()
            # return redirect('assignment_detail', pk=pk)
   
    cont={
        'works':works,
        'institution':institution,
        'school_id':school_id,
        'form':form
    }
    return render(request, 'templates/teacher/class_works.html', cont)

def class_work_result(request, pk, school_id):
    institution=get_institution(request, school_id)
    class_work = get_object_or_404(ClassWork, pk=pk)
    cont={
        'work':class_work,
        'institution':institution,
        'school_id':school_id,
    }
    return render(request, 'templates/teacher/class_work_result.html', cont)

def add_class_work_result(request, pk, school_id):
    institution=get_institution(request, school_id)
    class_work = get_object_or_404(ClassWork, pk=pk)
    form = ClassWorkResultForm()
    if request.method == 'POST':
        form = ClassWorkResultForm(request.POST)
        if form.is_valid():
            ass = form.save(commit=False)
            ass.class_work = class_work            
            ass.save()
        
    cont={
        'work':class_work,
        'institution':institution,
        'school_id':school_id,
        'form':form
    }
    return render(request, 'templates/teacher/work_result_form.html', cont)






def submission_create(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user.studentprofile  # Assuming user is a student
            submission.save()
            # Update gradebook
            gradebook, created = Gradebook.objects.get_or_create(student=submission.student, course=assignment.course)
            gradebook.update_average()
            return redirect('assignment_detail', pk=pk)
    else:
        form = SubmissionForm()
    return render(request, 'grades/submission_form.html', {'form': form})

def gradebook_list(request):
    gradebooks = Gradebook.objects.all()
    return render(request, 'grades/gradebook_list.html', {'gradebooks': gradebooks})

def gradebook_detail(request, pk):
    gradebook = get_object_or_404(Gradebook, pk=pk)
    report_card = gradebook.generate_report_card()
    return render(request, 'grades/gradebook_detail.html', {'report_card': report_card})

