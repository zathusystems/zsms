from main.utils import get_institution
from .views import expired
from subscription.models import SchoolSubscription, SubscriptionPlan
from django.shortcuts import render, redirect, get_object_or_404

def subs_plan(request, school_id):
    institution=get_institution(request, school_id)
    sub=SchoolSubscription.objects.get(school=institution)
    if not sub.is_active():
        return 'expired'
    return sub.plan.name

