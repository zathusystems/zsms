from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from attendance.models import StudentAttendance
from classroom.forms import ClassForm
from classroom.models import ClassRoom
from employee.models import Employee
from finance.models import Expense, Fee, FeePayment, Income, OtherFee
from finance.utils import total_balance, total_balance_this_month, total_expense_this_month, total_fee_this_month, total_income_this_month, total_other_income_month
from library.models import Book, BookCopy, Checkout
from notifications.forms import NoticeForm
from notifications.models import Notice
from school_calendar.forms import AcademicYearForm, TermForm
from school_calendar.models import AcademicYear, CalendarEvent, Term
from schooladminstration.forms import DepartmentForm, SchoolAddressForm
from staff_permision.permisions import can_manage_employees, can_manage_finances, can_manage_library, is_supper_admin
from student.models import Student
from subscription.models import SchoolSubscription
from teacher.forms import InstructorProfileForm
from teacher.models import LessonPlan
from timetable.models import TimeTable

from .utils import *
from django.http import JsonResponse
from main.utils import *
from datetime import datetime
from accounts.forms import CustomUserCreationForm, UpdateCustomUserForm, UserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

# Create your views here.
#redirect to waiting approval page
@login_required
def un_approved(request, school_id):
    # if request.user.parent:
    #     return redirect('parent:dash')
    if is_approved_account(request): return redirect('main:dashboard', school_id)
    institution=get_institution(request, school_id)
    cont={
        'institution':institution,
        'school_id':school_id,
    }
    return render(request, 'templates/main/un_approved_account.html', cont)

@login_required
def un_authorised(request, school_id):
    institution=get_institution(request, school_id)
    cont={
        'institution':institution,
        'school_id':school_id,
    }
    return render(request, 'templates/main/un_authrised.html', cont)



@login_required
def add_data(request, title, school_id):
    institution=get_institution(request, school_id)
    form = None
    card_title=None
    if title == 'add_academic_year':
        if institution.academic_year.all():
            return redirect('main:add_data', 'add_current_term', school_id)
        form = AcademicYearForm()
        card_title='add current academic year'
        if request.method == 'POST':
            form = AcademicYearForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.institution=institution
                d.save()
                return redirect('main:add_data', 'add_current_term', school_id)
            
    if title == 'add_current_term':
        if institution.terms.all():
            return redirect('main:add_data', 'add_contact_details', school_id)
        form = TermForm()
        academic_year=AcademicYear.objects.get(institution=institution, closed=False)
        card_title=f'Add current term/semister for {academic_year}'
        if request.method=='POST':
            form = TermForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.institution=institution
                d.academic_year=academic_year
                d.save()
                return redirect('main:add_data', 'add_contact_details', school_id)
            
            
    if title == 'add_contact_details':
        if institution.contact_details.all():
            return redirect('main:dashboard', school_id)
        form=SchoolAddressForm()
        card_title=f'Add Contact details'
        if request.method=='POST':
            form=SchoolAddressForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.school=institution
                d.save()
                return redirect('main:dashboard', school_id)
    cont={
        'institution':institution,
        'card_title':card_title,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/main/add_data.html', cont)


@login_required
def dashboard(request, school_id):
    if is_approved_account(request): pass
    else: return redirect('main:un_approved', school_id)
    
    institution=get_institution(request, school_id)
    if institution.academic_year.all(): pass 
    else: return redirect('main:add_data', 'add_academic_year', school_id)
    if institution.terms.all():pass
    else: return redirect('main:add_data', 'add_current_term', school_id)
    
    try: 
        if institution.subscription: pass 
    except: return redirect('subs:subscription_plans', school_id)
    
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    sub=SchoolSubscription.objects.get(school=institution)
    
    students=Student.objects.filter(school=institution)[0:8]
    teachers=Instructor.objects.filter(school=institution, approved=True)[0:8]
    teacher_requests=Instructor.objects.filter(school=institution, approved=False)
    classes=ClassRoom.objects.filter(school=institution)[0:8]
    attendance_list=StudentAttendance.objects.filter(school=institution).order_by('-date')[0:8]
    isadmin=False
    isclassteacher=False
    isribrarian=False
    ishr=False
    isaccountant=False
    if is_supper_admin(request):
        isadmin=True
    if can_manage_employees(request):
        ishr=True

    events=CalendarEvent.objects.filter(institution=institution).order_by('-start_date')[:3]
    #accountant dashboard
    fee_payments=FeePayment.objects.filter(school=institution).order_by('-payment_date')[0:6]
    incomes=Income.objects.filter(academic_year=academic_year)
    expenses=Expense.objects.filter(academic_year=academic_year)
    if can_manage_finances(request):
        isaccountant=True
    if is_class_teacher(request):
        isclassteacher=True

    #librarian dashboard
    all_books=0
    all_copies=0
    all_checked_out=0
    all_available=0
    book_copies=BookCopy.objects.filter(school=institution)
    book_list=Book.objects.filter(school=institution)
    checkouts=Checkout.objects.filter(school=institution).order_by('-checkout_date')
    if can_manage_library(request):
        all_books=Book.objects.filter(school=institution).count()
        all_copies=BookCopy.objects.filter(school=institution).count()
        all_checked_out=Checkout.objects.filter(school=institution, returned_date__isnull=True).count()
        all_available=all_copies-all_checked_out
        isribrarian=True

    time_table=TimeTable.objects.all()
    day_of_week=datetime.today().weekday()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = days[day_of_week]

    class_teacher=get_class_teacher(request)
    class_attendance_list=None
    classi=None
    classi_students=None
    lesson_plans=None
    if class_teacher:
        classi=ClassRoom.objects.get(teacher_assigned=class_teacher)
        lesson_plans = LessonPlan.objects.filter(teacher=class_teacher).order_by('-date')[0:8]
        class_attendance_list=StudentAttendance.objects.filter(class_room=classi).order_by('-date')[0:8]
        classi_students=classi.students.all()[0:8]
        
    employees=Employee.objects.filter(school=institution)
    
    term=Term.objects.get(institution=institution, closed=False)
    
    current_fees=Fee.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution)
  
    notes=Notice.objects.filter(school=institution).order_by('-created_at')
    date=datetime.today().date()
    cont={
        'students':students,
        'teachers':teachers,
        'classes':classes,
        'day':day,
        'is_admin':isadmin,
        'is_class_teacher':isclassteacher,
        'class':classi,
        'class_attendance_list':class_attendance_list,
        'attendance_list':attendance_list,
        'class_students':classi_students,
        'lesson_plans':lesson_plans,
        'is_teacher':is_teacher(request),
        'teacher_requests':teacher_requests,
        'current_fees':current_fees,

        'total_fees_this_month':total_fee_this_month(institution, date),
        'total_other_income_month':total_other_income_month(institution, date),
        'total_income_month':total_income_this_month(institution, date),
        'total_expense_month':total_expense_this_month(institution, date),
        'total_balance':total_balance(institution),


        # 'total_fees':total_fee_collected,
        # 'total_fee_year':total_fee_collected_this_year,
        # 'total_income_year':total_income_this_year,
        # 'total_expense_year':total_expense_this_year,
        # 'employees':employees,
        # 'overall_income':overall_income,
        # 'overall_expense':overall_expense,
        # 'total_expense':total_expense,
        # 'balance':overall_income-total_expense,
        
        
        'academic_year':academic_year,
        'is_hr':ishr,

        #accountant
        'fee_payments':fee_payments,
        'is_accountant':isaccountant,
        'expenses':expenses,
        'incomes':incomes,

        #hr manager
        'employees':employees,

        #librarian
        'is_librarian':isribrarian,
        'all_books':all_books,
        'all_copies':all_copies,
        'all_checked_out':all_checked_out,
        'all_available':all_available,
        'book_copies':book_copies,
        'book_list':book_list,
        'checkouts':checkouts,
        'current_school':institution.institution_name,

        'school_id':school_id,
        'institution':institution,
        'sub':sub,

        'notices':notes,
        'events':events
    }
    return render(request, 'templates/main/dashboard.html', cont)

@login_required()
def MyProfile(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved') 
    institution=get_institution(request, school_id)
    user_form = UpdateCustomUserForm(instance=request.user)
    profile_form=None
    prf=None
    if is_teacher(request):
        prf=Instructor.objects.get(user=request.user)
        profile_form = InstructorProfileForm(instance=prf)
    PassForm = PasswordChangeForm(request.user)
    
    if request.method == 'POST' and 'profile_edit' in request.POST:#name = profile_edit in submit button
        user_form = UpdateCustomUserForm(request.POST,instance=request.user)
        profile_form = InstructorProfileForm(request.POST, request.FILES, instance=prf)
        if user_form.is_valid:
            user_form.save()
            if profile_form.is_valid():
                profile_form.save()
            
    if request.method == 'POST' and 'change_pass_button' in request.POST:
        PassForm = PasswordChangeForm(user = request.user,data = request.POST)#i dnot see instance when changing password
        if PassForm.is_valid():
            PassForm.save()
            update_session_auth_hash(request, PassForm.user)  # Important!
            # messages.success(request,"Your password is successfully updated")
			# return redirect('register_app:user_view')
    if is_admin(request):
        profile_form=None
    cont={
        'user_form':user_form,
        'PassForm':PassForm,
        'profile_form':profile_form,
        'teacher':prf,
        'school_id':school_id,
        'institution':institution
    }
    return render(request,'templates/accounts/profile.html', cont)


def notice_board(request, school_id):
    if is_approved_account(request): pass 
    else: return redirect('main:un_approved', school_id)
    institution=get_institution(request, school_id)
    notes=Notice.objects.filter(school=institution).order_by('-created_at')
    form=NoticeForm()
    if request.method=='POST':
        form=NoticeForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.posted_by=request.user
            d.save()
    cont={
        'form':form, 
        'notices':notes,
        'school_id':school_id,
        'institution':institution
    }
    return render(request,'templates/notifications/notice_board.html', cont)



