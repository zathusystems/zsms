from django import forms
from .models import *


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = (
        'institution_name', 
        # 'phone',
        # 'country',
        # 'city',
        'edu_offer',
        'name_of_principal',
        'name_of_registrar',
        'name_of_head',

        )
    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)

        self.fields['institution_name'].widget.attrs.update({'class':'form-control'})
        self.fields['edu_offer'].widget.attrs.update({'class':'form-control'})
        self.fields['name_of_principal'].widget.attrs.update({'class':'form-control'})
        self.fields['name_of_registrar'].widget.attrs.update({'class':'form-control'})
        self.fields['name_of_head'].widget.attrs.update({'class':'form-control'})
        # self.fields['country'].widget.attrs.update({'class':'form-control'})
        # self.fields['city'].widget.attrs.update({'class':'form-control'})
        # self.fields['phone'].widget.attrs.update({'class':'form-control'})
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = (
        'title', 
        'description',
        )
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'title',
            # 'department',
            'description',
        )
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        # self.fields['department'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = (
            'title',
            # 'department',
            'description',
        )
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        # self.fields['department'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
    
class SchoolAddressForm(forms.ModelForm):
    class Meta:
        model = SchoolAddress
        fields = [
                'country',
                'city',
                'postal_code',
                'phone_number',
                'email',
                'address'
            ]
    def __init__(self, *args, **kwargs):
        super(SchoolAddressForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget.attrs.update({'class':'form-control'})
        self.fields['country'].widget.attrs.update({'class':'form-control'})
        self.fields['postal_code'].widget.attrs.update({'class':'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['address'].widget.attrs.update({'class':'form-control'})




