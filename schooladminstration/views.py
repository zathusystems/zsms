from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from parent.forms import ParentDetailsForm
from parent.models import Parent, ParentDetails, ParentStudentAccess
from student.models import Student
from .forms import *
from .models import *
from django.http import JsonResponse
from main.utils import *
from datetime import datetime
from notifications.utils import create_notif
# Create your views here.

# school profile views
@login_required
def school_info(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id) 
    institute=get_institution(request, school_id)
    form = InstitutionForm(instance=institute)
    addr=SchoolAddress.objects.get(school=institute)
    contact_form = SchoolAddressForm(instance=addr)
    if request.method=='POST' and 'save_info' in request.POST:
        if is_admin(request):
            form=InstitutionForm(request.POST, instance=institute)
            if form.is_valid():
                print('valid')
                form.save()
            else:
                print(form.errors)
        else:
            print('you cant change schoo info')

    elif request.method=='POST' and 'save_contact' in request.POST:
        if is_admin(request):
            contact_form=SchoolAddressForm(request.POST, instance=addr)
            if contact_form.is_valid():
                print('valid')
                contact_form.save()
            else:
                print(contact_form.errors)
        else:
        
            print('you cant change schoo info')
    cont={
        'form':form, 
        'contact_form':contact_form,
        'school_id':school_id, 
        'institution':institute
        }
    return render(request, 'templates/schooladmin/school_info.html', cont)

@login_required
def departments(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    departments=get_departments(request, school_id)
    
    form=DepartmentForm()
    if request.method=='POST':
        form=DepartmentForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.is_for=institution.edu_offer
            d.save()
        
    cont={
        'form':form,
        'departments':departments,
        'institution':institution,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/schooladmin/departments.html', cont)

@login_required
def department(request, d_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    department=Department.objects.get(id=d_id)
    form=None
    if institution.edu_offer=='tertialy education':
        form=CourseForm()
        if request.method=='POST':
            form=CourseForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.department=department
                d.save()
    else:
        form=SubjectForm()
        if request.method=='POST':
            form=SubjectForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.department=department
                d.is_for=institution.edu_offer
                d.save()
    cont={
        'form':form,
        'department':department,
        'institution':institution,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/schooladmin/department.html', cont)

def parents(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    parents=Parent.objects.all()
    parent_access=ParentStudentAccess.objects.filter(school__id=school_id)
    cont={
        'parents':parents,
        'parent_access_list':parent_access,
        'institution':institution,
        'school_id':school_id,
    }
    return render(request, 'templates/parent/parent_list.html', cont)

def add_parent_details(request, school_id, student_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    form=ParentDetailsForm()
    student=Student.objects.get(id=student_id)
    parent_d=ParentDetails.objects.filter(student=student).first()
    if parent_d:
        form=ParentDetailsForm(instance=parent_d)
    if request.method=='POST':
        if parent_d:
            form=ParentDetailsForm(request.POST, instance=parent_d)
            if form.is_valid():
                d=form.save(commit=False)
                d.student=student
                d.save()
        else:
            form=ParentDetailsForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.student=student
                d.save()

    cont={
        'form':form,
        'student':student,
        'institution':institution,
        'school_id':school_id,
        'parent_d':parent_d
    }
    return render(request, 'templates/schooladmin/add_parent_details.html', cont)


def parent(request, parent_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    parent=Parent.objects.get(id=parent_id)
    if request.method=='POST':
        access_id=request.POST.get('access_id')
        parent_access=ParentStudentAccess.objects.get(id=access_id)
        if 'approve' in request.POST:
            parent_access.approved=True
            parent_access.save()
            create_notif(
                'student access granted', 
                f'admins of <b>{institution}</b> has granted access of <b>{parent_access.student.first_name} {parent_access.student.last_name}</b> (student) information',
                parent_access.parent.user,
                institution,
                parent_access.parent.pk,
                True
                )
        if 'unapprove' in request.POST:
            parent_access.approved=False
            parent_access.save()
            create_notif(
                'student access denied', 
                f'admins of <b>{institution}</b> denied access of <b>{parent_access.student.first_name} {parent_access.student.last_name}</b> (student) information',
                parent_access.parent.user,
                institution,
                parent_access.parent.pk,
                True
                )
    cont={
        'parent':parent,
        'institution':institution,
        'school_id':school_id,
        'is_admin':is_admin(request)
    }
    return render(request, 'templates/parent/parent.html', cont)

def Staff(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    # if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    teachers=Instructor.objects.filter(school=institution)
    super_adm=institution.user
   
    cont={
        'teachers':teachers,
        'super_admin':super_adm,
        'school_id':school_id,
        'institution':institution,
        'school_id':school_id,
    }
    return render(request, 'templates/schooladmin/staff.html', cont)