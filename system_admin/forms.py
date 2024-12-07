from django import forms
from system_admin.models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'message', 'photo']

from system_admin.models import TeamMember

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'bio', 'photo', 'linkedin', 'twitter']

from system_admin.models import SystemFeature

class SystemFeatureForm(forms.ModelForm):
    class Meta:
        model = SystemFeature
        fields = ['title', 'description', 'icon']