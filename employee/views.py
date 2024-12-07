from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from finance.forms import ReconciliationForm
from finance.models import AdvancePayroll, PayrollReconciliation
from main.utils import get_institution, is_ajax, is_approved_account
from school_calendar.models import AcademicYear, Term
from staff_permision.permisions import can_manage_employees
from subscription.models import SchoolSubscription
from subscription.utils import subs_plan
from .models import AttendanceDate, Employee, EmployeeAttendance, LeaveRequest
from .forms import AttendanceDateForm, DocumentForm, EmployeeForm, leaveForm
from datetime import datetime
# from rest_framework import generics
# from .models import Employee
# from .serializers import EmployeeSerializer
# from .filters import EmployeeFilter
# from django_filters.rest_framework import DjangoFilterBackend


# class EmployeeListCreateView(generics.ListCreateAPIView):
#     serializer_class = EmployeeSerializer
#     serializer_class = EmployeeSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = EmployeeFilter

#     def get_queryset(self):
#         """
#         Optionally restrict the returned employees to a given school,
#         by filtering against a `school` query parameter.
#         """
#         queryset = Employee.objects.all()
#         school_id = self.request.query_params.get('school', None)
#         if school_id is not None:
#             queryset = queryset.filter(school_id=school_id)
#         return queryset




def employee_list(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_employees(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    employees = Employee.objects.filter(school=institution)
    form = EmployeeForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)

        form = EmployeeForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.save()
            
    cont={
        'form':form,
        'employees': employees,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/employee/employee_list.html', cont)

def employee_profile(request, employee_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_employees(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    employee = get_object_or_404(Employee, pk=employee_id)
    attendance_list = EmployeeAttendance.objects.filter(school=institution, employee=employee)
    leaves=LeaveRequest.objects.filter(employee=employee, school=institution)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee:employee_list', school_id)
   
    form = DocumentForm()
    cont={
        'attendance_list':attendance_list,
        'employee': employee,
        'school_id':school_id,
        'institution':institution,
        'leaves':leaves,
        'form':form
        }
    return render(request, 'templates/employee/employee_profile.html', cont)

def employee_update(request, employee_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_employees(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    employee = get_object_or_404(Employee, id=employee_id)
    form = EmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('../')
    return render(request, 'templates/employee/employee_form.html', {'form': form, 'institution':institution, 'school_id':school_id})

def employee_attendance_dates(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    institution=get_institution(request, school_id)
    attendance_dates = AttendanceDate.objects.filter(school=institution)
    form=AttendanceDateForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = AttendanceDateForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.save()
            return redirect('employee:mark_attendance', d.id, school_id)
    cont={
        'attendance_dates': attendance_dates,
        'form':form,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/employee/attendance_dates.html', cont)

def mark_employee_attendance(request, att_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
   
    print(datetime.today())
    employees=Employee.objects.filter(school=institution)

    already_marked=False
    if request.method=='POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        statuses=request.POST.getlist('status')
        employee_ids=request.POST.getlist('employee')
        atendance_date=AttendanceDate.objects.get(id=att_id)
        
        i=0
        for student_id in employee_ids:
            status=statuses[i]
            print(status, 'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
            student=Employee.objects.get(id=student_id)
            EmployeeAttendance.objects.create(
                school=institution,
                status=status, 
                attendance_date=atendance_date, 
                employee=student
                )
            i+=1
        
    cont={
        'employees':employees,
        'already_marked':already_marked,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/employee/mark_attendance.html', cont)

def attendance_list(request, att_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
  
    attendance_date=AttendanceDate.objects.get(id=att_id, school=institution)
    # atte_list=EmployeeAttendance.objects.filter(atendance_date=atendance_date)

    cont={
        'attendance_date':attendance_date,
        # 'already_marked':already_marked,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/employee/attendance_list.html', cont)


def payroll_reconciliation(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    dt=PayrollReconciliation.objects.filter(school=institution)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)         
    cont={
        'reconciliation':dt,
        'school_id':school_id
    }
    return render(request, 'templates/employee/reconciliation.html', cont)

def reconciliation_form(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    dt=PayrollReconciliation.objects.filter(school=institution)
    form=ReconciliationForm()
    employees=Employee.objects.filter(school=institution)
    year=datetime.today().year
    month=datetime.today().month
    print(month, 'kkkkkkkkkkkkkkkkkkkkkkkkkkk')

    if request.method=='POST':
        form=ReconciliationForm(request.POST)
        employee_id=request.POST.get('employee')
        employee=Employee.objects.get(id=employee_id)
        academic_year=AcademicYear.objects.get(institution=institution, closed=False)
        term=Term.objects.get(institution=institution, closed=False)
        if is_ajax(request):
            employee_salary=employee.salary
            attendance=EmployeeAttendance.objects.filter(employee=employee, processed=False, status='absent')
            paid_leaves=LeaveRequest.objects.filter(leave_type='unpaid', employee=employee,  processed=False,)
            dys=0
            for paid_leave in paid_leaves:
                dys+=paid_leave.total_days()
            try:
                adv=AdvancePayroll.objects.get(term=term, month=month, employee=employee)
            except:
                return JsonResponse({'salary':employee_salary, 'absent_days':abs(attendance.count()+dys)})
            return JsonResponse({'advance_salary':adv.amount, 'salary':employee_salary, 'absent_days':abs(attendance.count()+dys)})
        else:
            plan_name=subs_plan(request, school_id)
            if plan_name=='Free':return redirect('subs:upgrade', school_id)
            if plan_name=='expired':return redirect('subs:expired', school_id)
            if form.is_valid():
                d=form.save(commit=False)
                d.school=institution
                d.employee=employee
                d.month=datetime.today().month
                d.year=datetime.today().year
                d.academic_year=academic_year
                d.term=term
                d.save()
                attendance=EmployeeAttendance.objects.filter(employee=employee, processed=False, status='absent')
                paid_leaves=LeaveRequest.objects.filter(school=institution, leave_type='unpaid', employee=employee,  processed=False,)
                for att in attendance:
                    att.processed=True
                    att.save()
                for lvs in paid_leaves:
                    lvs.processed=True
                    lvs.save()
    cont={
        'reconciliation':dt,
        'form':form,
        'employees':employees,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/employee/reconciliation_form.html', cont)

def leave_list(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    leaves=LeaveRequest.objects.filter(school=institution).order_by('-start_date')

    return render(request, 'templates/employee/leave_employees.html', {'leaves': leaves, 'school_id':school_id, 'institution':institution})

def leave_add(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = leaveForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.save()
            return redirect('../')
    else:
        form = leaveForm()
    return render(request, 'templates/employee/leave_form.html', {'form': form, 'school_id':school_id, 'institution':institution})



def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'templates/employee/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee:employee_list')
    return render(request, 'templates/employee/employee_confirm_delete.html', {'employee': employee})
