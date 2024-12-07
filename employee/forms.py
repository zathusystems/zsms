
from django import forms
from .models import AttendanceDate, Employee, Document, LeaveRequest

class EmployeeForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        # label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    date_of_hire = forms.DateField(
        label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'address', 'position', 'employment_status', 'salary', 'date_of_hire']
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['gender'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['phone'].widget.attrs.update({'class':'form-control'})
        self.fields['position'].widget.attrs.update({'class':'form-control'})
        self.fields['employment_status'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['address'].widget.attrs.update({'class':'form-control'})
        self.fields['salary'].widget.attrs.update({'class':'form-control'})
        for fields2 in ['gender','first_name','last_name','position', 'date_of_birth', 'phone', 'address', 'salary', 'date_of_hire']:
            self.fields[fields2].help_text=None

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_type', 'document']
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['doc_type'].widget.attrs.update({'class':'form-control'})
        self.fields['document'].widget.attrs.update({'class':'form-control'})

class AttendanceDateForm(forms.ModelForm):
    date = forms.DateField(
        label='Date Of Attendance',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = AttendanceDate
        fields = ['date',]

class leaveForm(forms.ModelForm):
    start_date = forms.DateField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = LeaveRequest
        fields = ['employee','leave_status', 'leave_type', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(leaveForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({'class':'form-control select2'})
        self.fields['leave_status'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['leave_type'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['start_date'].widget.attrs.update({'class':'form-control'})
        self.fields['end_date'].widget.attrs.update({'class':'form-control'})
      