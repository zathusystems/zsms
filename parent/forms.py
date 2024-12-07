from django import forms
from .models import *


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = (
        'title',
        'phone',
        'address',
        'gender',
        )
    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['gender'].widget.attrs.update({'class':'form-control'})
        self.fields['address'].widget.attrs.update({'class':'form-control'})
        self.fields['phone'].widget.attrs.update({'class':'form-control'})

class ParentDetailsForm(forms.ModelForm):
    class Meta:
        model = ParentDetails
        fields = (
            'title',
            'first_name',
            'last_name',
            'phone',
            'address',
            'gender',
            'student'
        )
    def __init__(self, *args, **kwargs):
        super(ParentDetailsForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class':'form-control'})
        self.fields['address'].widget.attrs.update({'class':'form-control'})
        self.fields['phone'].widget.attrs.update({'class':'form-control'})

        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['student'].widget.attrs.update({'class':'form-control select2'})