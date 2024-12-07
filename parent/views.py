from django.shortcuts import get_object_or_404, render, redirect
from accounts.forms import UpdateCustomUserForm
from assignments.models import Assignment
from attendance.models import StudentAttendance, StudentAttendanceStatus
from exams.models import Result
from finance.models import Fee, FeeCategory, Invoice
from library.models import Checkout
from notifications.utils import create_notif
from parent.forms import ParentForm
from schooladminstration.models import Institution
from student.models import Enrollment, Student
from parent.models import Parent, ParentStudentAccess
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def search_id(request):
    students=None
    par=Parent.objects.get(user=request.user)
    q=False
    stu_d=None
    if request.method=='POST' and 'access' in request.POST:
        stu_id=request.POST.get('student_id','')
        student=Student.objects.get(id=stu_id)
        d=ParentStudentAccess()
        d.parent=par
        d.student=student
        d.school=student.school
        d.save()
        create_notif(
            'parent-student access request', 
            f'A parent is requesting access for {student}',
            student.school.user,
            student.school,
            d.id,
            False
        )
        return redirect('parent:children')
    elif request.method=='POST':
        q=True
        stu_d=request.POST.get('id_number','')
        if stu_d:
            students=Student.objects.filter(id_number=stu_d)
    cont={
        'students':students,
        'parent':par,
        'stu_id':stu_d,
        'q':q
        }
    return render(request, 'templates/parent/confirm_child.html', cont)

def dashboard(request):
    par=Parent.objects.get(user=request.user)
    chldrn=ParentStudentAccess.objects.filter(parent=par)
    attendance=StudentAttendance.objects.all()

    cont={
        'children':chldrn,
        'parent':par,
        'attendance':attendance
        }
    return render(request, 'templates/parent/dashboard.html', cont)

def children(request):
    par=Parent.objects.get(user=request.user)
    chldrn=ParentStudentAccess.objects.filter(parent=par)
    cont={
        'children':chldrn,
        'parent':par,
        }
    return render(request, 'templates/parent/children.html', cont)

def child_info(request, student_id):
    par=Parent.objects.get(user=request.user)
    child=ParentStudentAccess.objects.get(student__id=student_id)
    attendance=StudentAttendanceStatus.objects.filter(student=child.student)
    enrollement=Enrollment.objects.get(student=child.student)
    cate=FeeCategory.objects.get(enrollment=enrollement)
    fee=Fee.objects.filter(fee_category=cate).last()
    fee=Fee.objects.filter(fee_category=cate).last()
    cont={
        'child':child.student,
        'student':child.student,
        'parent':par,
        'attendance':attendance,
        'enrollement':enrollement,
        'fee_category':cate,
        'fee':fee
        }
    return render(request, 'templates/parent/child_info.html', cont)

def exam_result(request, student_id):
    par=Parent.objects.get(user=request.user)
    child=ParentStudentAccess.objects.get(student__id=student_id)
    examresult=Result.objects.filter(student=child.student).order_by('-date')

    # attendance=StudentAttendanceStatus.objects.filter(student=child.student)
    # enrollement=Enrollment.objects.get(student=child.student)
    # cate=FeeCategory.objects.get(enrollment=enrollement)
    # fee=Fee.objects.filter(fee_category=cate).last()
    cont={
        'student':child.student,
        'parent':par,
        'examresults':examresult
        # 'attendance':attendance,
        # 'enrollement':enrollement,
        # 'fee_category':cate,
        # 'fee':fee
        }
    return render(request, 'templates/parent/exam_result.html', cont)

   
def attendance(request, student_id):
    par=Parent.objects.get(user=request.user)
    child=ParentStudentAccess.objects.get(student__id=student_id)
    attendance=StudentAttendanceStatus.objects.filter(student=child.student)
    # attendance=StudentAttendanceStatus.objects.filter(student=child.student)
    # enrollement=Enrollment.objects.get(student=child.student)
    # cate=FeeCategory.objects.get(enrollment=enrollement)
    # fee=Fee.objects.filter(fee_category=cate).last()
    cont={
        'student':child.student,
        'child':child,
        'parent':par,
        'attendance':attendance,
        # 'enrollement':enrollement,
        # 'fee_category':cate,
        # 'fee':fee
        }
    return render(request, 'templates/parent/attendance.html', cont)


def book_checkouts(request, student_id):
    c_outs=Checkout.objects.filter(student__id=student_id)
    child=ParentStudentAccess.objects.get(student__id=student_id)
    cont={
        'checkouts':c_outs,
        'child':child,
    }
    return render(request, 'templates/parent/boo_checkouts.html', cont)

def assignments(request, student_id):
    student=get_object_or_404(Student, id=student_id)
    assignments = Assignment.objects.filter(classi=student.class_students.first())
    cont={
        'assignments':assignments,
        'student':student
    }
    return render(request, 'templates/parent/assignments.html', cont)


def schools(request):
    par=Parent.objects.get(user=request.user)
    parent_accesses=ParentStudentAccess.objects.filter(parent=par)
    cont={
        'parent_accesses':parent_accesses,
    }
    return render(request, 'templates/parent/schools.html', cont)

def school_info(request, school_id):
    par=Parent.objects.get(user=request.user)
    school=Institution.objects.get(id=school_id)
    cont={
        'parent':par,
        'school':school
        }
    return render(request, 'templates/parent/school_info.html', cont)


def invoices(request):
    par=Parent.objects.get(user=request.user)
    child=ParentStudentAccess.objects.get(parent=par)
    invoices=Invoice.objects.filter(student=child.student)

    cont={
        # 'invoices':school_id,
        # 'institution':institution,
        'invoices':invoices
    }
    return render(request, 'templates/parent/invoicing.html', cont)

def invoice_view(request, inv_id):
    invoice=Invoice.objects.get(id=inv_id)
    cont={
        'invoice':invoice,
    }
    return render(request, 'templates/parent/invoice_view.html', cont)

def become_parent(request):
    try:
        par=Parent.objects.get(user=request.user)
        return redirect('parent:dash')
    except:
        pass
    form=ParentForm()
    if request.method == 'POST':
        form=ParentForm(request.POST)
        print('ggggggggggggggggggggggggggggg')
        if form.is_valid():
            print('ggggggggggggggggggggggggggggg222222222222222222')
            d=form.save(commit=False)
            d.user=request.user
            d.save()
            return redirect('parent:dash')
        
        print(form.is_valid(), 'gggggggggggggggggggggggggggggggggnnnnnnnnnnnnnnnnnnnnnnn')
    # chldrn=ParentStudentAccess.objects.filter(parent=par)
    # attendance=StudentAttendance.objects.all()

    cont={
        'form':form,
        }
    return render(request, 'templates/parent/become_parent.html', cont)


@login_required()
def MyProfile(request):
    user_form = UpdateCustomUserForm(instance=request.user)
    par=Parent.objects.get(user=request.user)
    parent_form=ParentForm(instance=par)
    PassForm = PasswordChangeForm(request.user)
    
    if request.method == 'POST' and 'profile_edit' in request.POST:#name = profile_edit in submit button
        user_form = UpdateCustomUserForm(request.POST,instance=request.user)
        parent_form = ParentForm(request.POST, request.FILES, instance=par)
        if user_form.is_valid:
            user_form.save()
            if parent_form.is_valid():
                parent_form.save()
            
    if request.method == 'POST' and 'change_pass_button' in request.POST:
        PassForm = PasswordChangeForm(user = request.user,data = request.POST, autofocus=False)#i dnot see instance when changing password
        if PassForm.is_valid():
            PassForm.save()
            update_session_auth_hash(request, PassForm.user)  # Important!
            # messages.success(request,"Your password is successfully updated")
			# return redirect('register_app:user_view')
    # if is_admin(request):
    #     profile_form=None
    cont={
        'user_form':user_form,
        'PassForm':PassForm,
        'parent_form':parent_form,
        'parent':par,
    }
    return render(request,'templates/parent/profile.html', cont)