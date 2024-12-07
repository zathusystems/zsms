from re import template
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUp, name='signup'),
    path('login/', Login, name='login'),
    path('profile-selection/', profile_select_view, name='profile_select'),
    path('create', create_teacher, name='create_teacher'),

    path('confirm_email', Confirm_signup, name='confirm_si'),
    path('email_confirmed', Confirmed_signup, name='confirmed_si'),
    path('logout', logout_view, name='logout'),
    path('school-profiles', school_profiles, name='school_p'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset/', ForgetPassword, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password/password_reset_confirm.html"), name='password_reset_confirm'),
    ]