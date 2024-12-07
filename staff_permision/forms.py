from django import forms
from .models import Permision


class PermisionForm(forms.ModelForm):
    is_supper_admin=forms.CharField(
        help_text='User is granted full access of your data',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class':'form-control',
              
            }
        )
    )
    class Meta:
        model = Permision
        fields = ['is_supper_admin', 'is_admin', 'can_manage_employees', 'can_manage_finances', 'can_manage_library']
    def __init__(self, *args, **kwargs):
        super(PermisionForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs.update({'class':'form-control'})
        # self.fields['author'].widget.attrs.update({'class':'form-control'})
        # self.fields['description'].widget.attrs.update({'class':'form-control'})
        # self.fields['isbn'].widget.attrs.update({'class':'form-control'})