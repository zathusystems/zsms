from django import forms
from .models import Exam, ExamDate, ExamSubjects, Result

class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = ['title']
        
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        # self.fields['classes'].widget.attrs.update({'class':'form-control selectric', 'multiple':''})
        
        
class ExamDateForm(forms.ModelForm):
    exam_date = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    
    class Meta:
        model = ExamDate
        fields = ['exam_date']
        
    def __init__(self, *args, **kwargs):
        super(ExamDateForm, self).__init__(*args, **kwargs)
        # self.fields['classes'].widget.attrs.update({'class':'form-control selectric', 'multiple':''})
        

class ExamSubjectsForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'time'
            }))
    end_time = forms.TimeField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'time'
            }))
    class Meta:
        model = ExamSubjects
        fields = ['subject', 'title', 'start_time', 'end_time', 'total_marks']
    def __init__(self, *args, **kwargs):
        super(ExamSubjectsForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['total_marks'].widget.attrs.update({'class':'form-control'})
        
        
class ExamResultsForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['marks_obtained']
    def __init__(self, *args, **kwargs):
        super(ExamResultsForm, self).__init__(*args, **kwargs)
        # self.fields['student'].widget.attrs.update({'class':'form-control select2', 'style':'width:100%'})
        self.fields['marks_obtained'].widget.attrs.update({'class':'form-control', 'max':'100'})
