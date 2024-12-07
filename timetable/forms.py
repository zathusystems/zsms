from django import forms
from .models import *

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = (
            'title',
            # 'classes',
        )
    def __init__(self, *args, **kwargs):
        super(TimeTableForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        # self.fields['classes'].widget.attrs.update({'class':'form-control select2', 'style'})
        
class TimeTableSubjectForm(forms.ModelForm):
    start_time = forms.TimeField(
        label='Starting Time',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'time'
            }
        )
    )
    end_time = forms.TimeField(
        label='Ending Time',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'time'
            }
        )
    )
    class Meta:
        model = TimeTableSubjects
        fields = (
            'day',
            'subject',
            'start_time',
            'end_time'
        )
    def __init__(self, *args, **kwargs):
        super(TimeTableSubjectForm, self).__init__(*args, **kwargs)
        self.fields['day'].widget.attrs.update({'class':'form-control selectric'})
        self.fields['subject'].widget.attrs.update({'class':'form-control selectric'})
