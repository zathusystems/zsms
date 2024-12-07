from django import forms

from school_calendar.models import AcademicYear, Term

class AcademicYearForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    end_date = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    class Meta:
        model = AcademicYear
        fields = ['year', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(AcademicYearForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class':'form-control'})
        
        
class TermForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    end_date = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    class Meta:
        model = Term
        fields = ['title', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})

# forms.py
from django import forms
from .models import CalendarEvent

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'description', 'event_type', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.SelectDateWidget(),
            'end_date': forms.SelectDateWidget(),
        }
    def __init__(self, *args, **kwargs):
        super(CalendarEventForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs.update({'class':'form-control'})