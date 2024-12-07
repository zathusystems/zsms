from .models import Permision
from main.utils import is_admin
def permision(request):
    try:
        permisio=Permision.objects.get(user=request.user)
        return permisio
    except: return None

def is_supper_admin(request):
    p=permision(request)
    if p:
        if p.is_supper_admin:return True
    elif is_admin(request):
        return True
    return False

def is_staff(request):
    p=permision(request)
    if p:
        if p.is_admin:return True
    elif is_admin(request):
        return True
    return False

def can_manage_employees(request):
    p=permision(request)
    if p:
        if p.can_manage_employees:return True
    elif is_admin(request):
        return True
    return False

def can_manage_finances(request):
    p=permision(request)
    if p:
        if p.can_manage_finances:return True
    elif is_admin(request):
        return True
    return False
    
def can_manage_library(request):
    p=permision(request)
    if p:
        if p.can_manage_library:return True
    elif is_admin(request):
        return True
    return False