from django.shortcuts import get_object_or_404, redirect
from schooladminstration.models import Department, Institution
from teacher.models import Instructor
from django.contrib.auth.decorators import user_passes_test

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH')=='XMLHttpRequest'

def get_institution(request, school_id):
    istitution=get_object_or_404(Institution, id=school_id)
    return istitution
    
def get_departments(request, school_id):
    institution=get_institution(request, school_id)
    departments=None
    if institution.edu_offer=='secondary education':
        departments=Department.objects.filter(is_for=institution.edu_offer)
    else:
        departments=Department.objects.all()
    return departments
    
def is_admin(request):
    try:
        institution=get_object_or_404(Institution, user=request.user)
        if institution:
            return True
    except:
        return False
    
def is_class_teacher(request):
    try:
        instructor=get_object_or_404(Instructor, user=request.user)
        if instructor.assigned_class.all():
            return True
    except:
        return False
    
def is_teacher(request):
    try:
        instructor=get_object_or_404(Instructor, user=request.user)
        if instructor:
            return True
    except:
        return False
    
def get_instructor(request):
    try:
        instructor=get_object_or_404(Instructor, user=request.user)
        if instructor:
            return instructor
    except:
        return None
    
def get_class_teacher(request):
    try:
        instructor=get_object_or_404(Instructor, user=request.user)
        if instructor.assigned_class.all():
            return instructor
    except:
        return None
    
def is_approved_account(request):
    if is_teacher(request):
        instructor=get_instructor(request)
        if instructor.approved:
            return True
        else:
            return False
    elif is_admin(request):
        return True
    
