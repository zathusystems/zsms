
from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
        'first_name', 
        'last_name',
        'gender',
        'phone',
        'id_number',
        'address',
        )
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['gender'].widget.attrs.update({'class':'form-control select2'})
        self.fields['id_number'].widget.attrs.update({'class':'form-control'})
        self.fields['address'].widget.attrs.update({'class':'form-control'})
        self.fields['phone'].widget.attrs.update({'class':'form-control'})

        
class EnrollmentForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Enrollment Date',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = Enrollment
        fields = (
        'department',
        'courses',
        'subjects',
        'start_date',
        'status',
        )
    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['department'].widget.attrs.update({'class':'form-control select2'})
        self.fields['courses'].widget.attrs.update({'class':'form-control select2', 'multiple':''})
        self.fields['subjects'].widget.attrs.update({'class':'form-control select2', 'multiple':'', 'style':'width 100%'})
        self.fields['status'].widget.attrs.update({'class':'form-control select2'})
