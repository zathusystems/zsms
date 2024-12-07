import email
from pyexpat.errors import messages
from accounts.models import CustomUser
from notifications.utils import create_notif
from parent.forms import ParentForm
from parent.models import Parent
from schooladminstration.models import Institution
from student.models import Student
from teacher.forms import InstructorForm, SelectInstructorProfileForm
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from .token import account_activation_token, generate_code
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from json import dumps as jdumps
from django.contrib.auth import logout

from teacher.models import Instructor
from schooladminstration.forms import InstitutionForm

# Create your views here.

#user login
def Login(request):
    form = AuthenticationForm()
    print(request.path, 'kkkkkkkkk')
    next=None
    if request.method != 'POST':
        next=request.GET.get('next')
        request.session['next']=next
    
    if request.user.is_authenticated:
        return redirect('accounts:school_p')
    else:
        print('ok')
        if request.method == 'POST':
            email = request.POST.get('email','')
            password = request.POST.get('password','')
            print(email, password)
            user=authenticate(request, email=email, password=password)
        
            if user is not None:
                login(request, user)
                nxt=request.session.get('next')
                return JsonResponse({'status':'loggedin', 'next':nxt})
            
            else:
                print('response2')
                return JsonResponse({'status':'failed'})
        else:
            form = AuthenticationForm()
    cont = {
        'form': form
    }
    return render(request, 'templates/accounts/login.html', cont)

    
# create user account
def SignUp(request):
    if request.user.is_authenticated:
        return redirect('accounts:school_p')
    form=CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            fn = request.POST.get('first_name','')
            ln = request.POST.get('last_name','')
            password = request.POST.get('password1','')
            user = form.save(commit=False)
            user.first_name = fn
            user.last_name = ln
            user.is_active = True
            user.save()

            us=authenticate(request, email=user.email, password=password)
            print(password, user.email)
            if us is not None:
                login(request, user)
            # redirect user
            return JsonResponse({'status':'succeed'})

        else:
            error_msg=""
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
                    error_msg+=f"{error} <br>"
        
            return JsonResponse({'status':'failed', 'error_msg':error_msg})

    else:
        form = CustomUserCreationForm()
    return render(request, 'templates/accounts/signup.html', {'form': form})


# reset user password
def ForgetPassword(request):
    password_reset_form = PasswordResetForm()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_mail=request.POST.get('email')
            u=get_user_model()
            if not u.objects.filter(email=user_mail).first():
                 messages.success(request, 'No account mached your email')
                 print('No account mached your email')

            current_site = get_current_site(request)
            user_obj=u.objects.get(email=user_mail)
            mail_subject = "Password Reset Requested"
            message = render_to_string('accounts/password/password_reset_email.txt', {
                'user': user_obj,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user_obj.pk)),
                'token':default_token_generator.make_token(user_obj),
                'protocol': 'http',
            })
            email = EmailMessage(mail_subject, message, to=[user_obj.email] )
            try:
                email.send()
                print('email sent')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('password_reset_done')
    password_reset_form = PasswordResetForm()
    return render(request, 'accounts/password/password_reset.html', {'password_reset_form':password_reset_form})


# comfirm account email
def Confirm_signup(request):
    return render(request, 'accounts/confirm_signup.html')

# account email comfirmed
def Confirmed_signup(request):
    return render(request, 'accounts/confirmed_signup.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# profile selection views
def profile_select_view(request):
    print('22222222222222222222222222222222222222222', request.user.first_name, request.user.last_name)
    form=SelectInstructorProfileForm()
    form2=InstitutionForm()
    parent_form=ParentForm()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=SelectInstructorProfileForm()
            form2 = InstitutionForm(request.POST)
            parent_form=ParentForm(request.POST)
            if form2.is_valid():
                # save form in the memory not in database
                name = request.POST.get('institution_name','')
                country = request.POST.get('country','')
                city = request.POST.get('city','')
                phone = request.POST.get('phone','')
                edu = request.POST.get('edu_offer','')
                n_princ = request.POST.get('name_of_principal','')
                n_head = request.POST.get('name_of_head','')
                n_regi = request.POST.get('name_of_registrar','')

                institution = form2.save(commit=False)
                institution.user = request.user
                institution.intstitution_name = name
                institution.country = country
                institution.city = city
                institution.phone = phone
                institution.edu_offer = edu
                institution.name_of_principal = n_princ
                institution.name_of_head = n_head
                institution.name_of_registrar = n_regi
                institution.save()
                return JsonResponse({'status':'succeed', 'school_id':institution.id})
            elif form.is_valid():
                gender = request.POST.get('gender','')
                phone = request.POST.get('phone','')
                school = request.POST.get('school','')
                role = request.POST.get('role','')
                title = request.POST.get('title','')
                teacher=form.save(commit=False)
                teacher.gender=gender
                teacher.phone=phone
                teacher.school=school
                teacher.role=role
                teacher.title=title
                teacher.save()
                return JsonResponse({'status':'succeed', 'school_id':school.id})
            elif parent_form.is_valid():
                stu_d=request.POST.get('id_number','')
                students=Student.objects.filter(id_number=stu_d)
                if stu_d:q=True
                else:q=False
                try:
                    par=Parent.objects.get(user=request.user)
                    cont={
                    'sudents':students,
                    'parent':par,
                    'q':q
                    }
                    return render(request, 'templates/parent/confirm_child.html', cont)
                except:
                    d=parent_form.save(commit=False)
                    d.user=request.user
                    d.save()
                    cont={
                        'sudents':students,
                        'parent':d,
                        'q':q
                    }
                    
                    return render(request, 'templates/parent/confirm_child.html', cont)

            
            else:
                error_msg=""
                for field, errors in form2.errors.items():
                    for error in errors:
                        print(f"Error in {field}: {error}")
                        error_msg+=f"{error} <br>"

                return JsonResponse({'status':'failed', 'error_msg':error_msg})
    else:
        return redirect('accounts:login')
    return render(request, 'templates/accounts/profile_select.html', {'form1':form, 'form2':form2, 'parent_form':parent_form})


# profile selection views
def create_teacher(request):
    print('111111111111111111111111111')
    form=SelectInstructorProfileForm()
    if request.method == 'POST':
        form=SelectInstructorProfileForm(request.POST)
        if form.is_valid():
            print('valid')
            gender = request.POST.get('gender','')
            phone = request.POST.get('phone','')
            school_id = request.POST.get('school','')
            date_started = request.POST.get('date_started','')
            teacher=form.save(commit=False)
            teacher.gender=gender
            teacher.phone=phone
            teacher.first_name=request.user.first_name
            teacher.last_name=request.user.last_name
            teacher.date_started=date_started
            teacher.school=Institution.objects.get(id=school_id)
            teacher.user=request.user
            teacher.save()
            return JsonResponse({'status':'succeed'})
        else:
            print('not')
            error_msg=""
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
                    error_msg+=f"{error} <br>"
            return JsonResponse({'status':'failed', 'error_msg':error_msg})

    return render(request, 'templates/accounts/profile_select.html', {'form1':form})

from django.contrib.auth.decorators import login_required
@login_required
def school_profiles(request):
    schools=Institution.objects.filter(user=request.user)
    form=InstitutionForm()
    if request.user.instructor_profile.all():
        print(';kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk11111111111')
        instr=Instructor.objects.get(user=request.user)
        sch=instr.school
        return redirect('main:dashboard', sch.id)
    
    elif request.user.parent.all():
        print(';kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk222222')
        return redirect('parent:dash')
    else:
        pass
    
    if request.method == 'POST':
        form=InstitutionForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.user = request.user
            d.save()
            # return redirect('main:dashboard')
    cont={
        'schools':schools,
        'form':form
    }
    return render(request, 'templates/accounts/school_profiles.html', cont)