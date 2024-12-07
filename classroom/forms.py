from django import forms
from .models import *

class ClassForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = (
        'class_name',
        # 'teacher_assigned'
        )
    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['class_name'].widget.attrs.update({'class':'form-control'})
        # self.fields['teacher_assigned'].widget.attrs.update({'class':'form-control select2'})


class ClassForm2(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = (
        'class_name',
        'teacher_assigned'
        )
    def __init__(self, *args, **kwargs):
        super(ClassForm2, self).__init__(*args, **kwargs)
        self.fields['class_name'].widget.attrs.update({'class':'form-control'})
        self.fields['teacher_assigned'].widget.attrs.update({'class':'form-control select2'})