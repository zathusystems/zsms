from django import forms
from .models import *
from assignments.models import Submission, Assignment, ClassWork, ClassWorkResult

class InstructorForm(forms.ModelForm):
    date_started = forms.DateField(
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
        model = Instructor
        fields = (
        'date_started',
        'role',
        'first_name', 
        'last_name',
        'phone',
        'gender',
        'department',
        'subjects_taught',
        'courses_taught',
        'approved'
        )
    def __init__(self, *args, **kwargs):
        super(InstructorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['role'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['phone'].widget.attrs.update({'class':'form-control'})
        self.fields['gender'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['subjects_taught'].widget.attrs.update({'class':'form-control selectric', 'multiple':''})
        self.fields['courses_taught'].widget.attrs.update({'class':'form-control selectric', 'multiple':''})
        self.fields['department'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['approved'].widget.attrs.update({'class':'custom-checkbox'})

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = (
        'phone',
        # 'gender',
        # 'department',
        # 'subjects_taught',
        # 'courses_taught',
        )
    def __init__(self, *args, **kwargs):
        super(InstructorProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({'class':'form-control'})
        # self.fields['gender'].widget.attrs.update({'class':'form-control selectric'})
        # self.fields['department'].widget.attrs.update({'class':'form-control selectric'})
        # self.fields['subjects_taught'].widget.attrs.update({'class':'form-control selectric', 'multiple':''})
        # self.fields['courses_taught'].widget.attrs.update({'class':'form-control selectric', 'multiple':''})

class SelectInstructorProfileForm(forms.ModelForm):
    date_started = forms.DateField(
        label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        # required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = Instructor
        fields = (
        'title',
        'gender',
        'role',
        'phone',
        'school',
        'date_started'
        )
    def __init__(self, *args, **kwargs):
        super(SelectInstructorProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({'class':'form-control'})
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['role'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%;' })
        self.fields['gender'].widget.attrs.update({'class':'form-control select2'})
        self.fields['school'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%;' })

from .models import LessonPlan, Gradebook

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['title', 'description', 'objectives', 'materials_needed', 'content', 'date']
    def __init__(self, *args, **kwargs):
        super(LessonPlanForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['objectives'].widget.attrs.update({'class':'form-control'})
        self.fields['materials_needed'].widget.attrs.update({'class':'form-control'})
        self.fields['content'].widget.attrs.update({'class':'form-control'})
        self.fields['date'].widget.attrs.update({'class':'form-control'})


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = Assignment 
        fields = ['classi', 'subject', 'title', 'description', 'total_marks', 'due_date']
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['classi'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%'})
        self.fields['subject'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%'})
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['total_marks'].widget.attrs.update({'class':'form-control'})

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission 
        fields = ['student', 'marks', 'comment']
    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class':'form-control select2'})
        self.fields['marks'].widget.attrs.update({'class':'form-control'})
        self.fields['comment'].widget.attrs.update({'class':'form-control'})




class ClassWorkForm(forms.ModelForm):
    class Meta:
        model = ClassWork 
        fields = ['classi', 'subject', 'number_of_questions']
    def __init__(self, *args, **kwargs):
        super(ClassWorkForm, self).__init__(*args, **kwargs)
        self.fields['classi'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%'})
        self.fields['subject'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%'})
        # self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['number_of_questions'].widget.attrs.update({'class':'form-control'})

class ClassWorkResultForm(forms.ModelForm):
    class Meta:
        model = ClassWorkResult
        fields = ['student', 'marks', 'comment']
    def __init__(self, *args, **kwargs):
        super(ClassWorkResultForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class':'form-control select2'})
        self.fields['marks'].widget.attrs.update({'class':'form-control'})
        self.fields['comment'].widget.attrs.update({'class':'form-control'})













class GradebookForm(forms.ModelForm):
    class Meta:
        model = Gradebook
        fields = ['student', 'course']