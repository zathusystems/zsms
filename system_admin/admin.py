from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import * 

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'created_at']
    search_fields = ['name', 'role', 'message']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    search_fields = ['name', 'position']

@admin.register(SystemFeature)
class SystemFeatureAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title', 'description']

admin.site.register(Contact)
admin.site.register(About)
admin.site.register(Terms)
admin.site.register(Privacy)
admin.site.register(Faqs)
