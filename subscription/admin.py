from django.contrib import admin
from .models import SubscriptionPlan, Feature, SchoolSubscription

# @admin.register(SubscriptionPlan)
# class SubscriptionPlanAdmin(admin.ModelAdmin):
#     list_display = ['name', 'price', 'duration_in_days']
#     search_fields = ['name']

# @admin.register(Feature)
# class SchoolAdmin(admin.ModelAdmin):
#     list_display = ['plan', 'feature', 'subscription', 'subscription_start_date', 'subscription_end_date']
#     search_fields = ['name', 'owner__username']
admin.site.register(SubscriptionPlan)
admin.site.register(Feature)
admin.site.register(SchoolSubscription)
