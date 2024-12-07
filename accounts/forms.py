from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from schooladminstration.models import Institution


class CustomUserCreationForm(UserCreationForm):
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    email=forms.EmailField(max_length=250)
    class Meta:
        model=get_user_model()
        fields=('first_name','last_name','email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
        for fields2 in ['email','first_name','last_name','password1', 'password2']:
            self.fields[fields2].help_text=None


class UpdateCustomUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name')

    def __init__(self, *args, **kwargs):
         super(UpdateCustomUserForm, self).__init__(*args, **kwargs)
         self.fields['first_name'].widget.attrs.update({'class':'form-control'})
         self.fields['last_name'].widget.attrs.update({'class':'form-control'})
         for fields2 in ['first_name','last_name']:
             self.fields[fields2].help_text=None


class UserProfileForm(forms.ModelForm):
    class Meta:
        #model=UserProfile
        fields=(
            'gender',
            'profile_pic',

        )
        


class InstitutionForm(forms.ModelForm):
    class Meta:
        model=Institution
        fields=(
            'country',
            'city',
        )