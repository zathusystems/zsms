from django import forms
from .models import *

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ( 
        'course',
        'subject',
        )
    def __init__(self, *args, **kwargs):
        super(StudentAttendanceForm, self).__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.update({'class':'form-control select2'})
        self.fields['subject'].widget.attrs.update({'class':'form-control select2'})