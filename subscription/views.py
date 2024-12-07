from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from main.utils import get_institution, is_admin, is_ajax, is_approved_account
from subscription.init_payment import initiate_payment
from .models import SubscriptionPayments, SubscriptionPlan, SchoolSubscription, Feature
from schooladminstration.models import Institution as School


def upgrade(request, school_id):
    institution=get_institution(request, school_id)
    cont={
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/subscription/upgrade.html', cont)

def expired(request, school_id):
    institution=get_institution(request, school_id)
    cont={
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/subscription/expired.html', cont)

# View to list available subscription plans
def subscription_plans(request, school_id):
    plans = SubscriptionPlan.objects.all()
    features=Feature.objects.all()
    school = get_object_or_404(School, id=school_id)  
    cont={'plans': plans, 'institution': school, 'school_id':school_id, 'features':features}
    return render(request, 'templates/subscription/plans.html', cont)

def after_payment_success(request, plan_id, school_id, sub_type, period):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    school = get_object_or_404(School, id=school_id)  
    sub=sub_type
    if sub=='trial':pass 
    else: sub=None
    # period=request.POST.get('period')
    try:
        subs=SchoolSubscription.objects.get(school=school)
        if plan.name=='Free':pass
        else:
            if sub_type == 'trial' and not school.tried_subscription: 
                    subs.is_trial = True
                    subs.end_date = timezone.now() + timezone.timedelta(30)
                    school.tried_subscription=True
                    school.save()
            else: 
                    subs.is_trial = False

                    # if subs.plan == plan:
                    if subs.plan.name=='Free':
                        if period=='monthly':
                            subs.end_date = timezone.now() + timezone.timedelta(days=30)
                        elif period == 'half_year':
                            subs.end_date = timezone.now() + timezone.timedelta(days=182)
                        elif period == 'yearly':
                            subs.end_date = timezone.now() + timezone.timedelta(days=364)
                    else:
                        if period=='monthly':
                            subs.end_date = timezone.now() + timezone.timedelta(days=30+subs.remaining_days())
                        elif period == 'half_year':
                            subs.end_date = timezone.now() + timezone.timedelta(days=182+subs.remaining_days())
                        elif period == 'yearly':
                            subs.end_date = timezone.now() + timezone.timedelta(days=364+subs.remaining_days())
                        
            subs.plan=plan
            subs.save()
            return redirect('subs:sub_success', plan_id, school.id, sub_type)
    except:
            subs=SchoolSubscription()
            subs.school=school
            subs.plan=plan
            if plan.name=='Free':
                pass
            else:    
                if sub_type == 'trial' and not school.tried_subscription: 
                    subs.end_date = timezone.now() + timezone.timedelta(days=30)  # 30-day trial
                    subs.is_trial = True
                    school.tried_subscription=True
                    school.save()
                else: 
                    subs.is_trial = False
                    price=0
                    if period=='monthly':
                        subs.end_date = timezone.now() + timezone.timedelta(days=30)
                        price=subs.plan.price
                    elif period == 'half_year':
                        subs.end_date = timezone.now() + timezone.timedelta(days=182)
                        price=subs.plan.half_year_price
                    elif period == 'yearly':
                        subs.end_date = timezone.now() + timezone.timedelta(days=364)
                        price=subs.plan.yearly_price

                   
            subs.save()
            return redirect('subs:sub_success', plan_id, school.id, sub_type)

# View to allow a school to subscribe or upgrade to a plan
def subscribe_to_plan(request, plan_id, school_id, sub_type):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    school = get_object_or_404(School, id=school_id)  
    sub=sub_type
    if sub=='trial':pass 
    else: sub=None
    if is_ajax(request):
        if request.method == 'POST':
            period=request.POST.get('period')
            if period=='monthly':
                return JsonResponse({'price':plan.price,})
            elif period == 'half_year':
                return JsonResponse({'price':plan.half_year_price,})
            elif period == 'yearly':
                return JsonResponse({'price':plan.yearly_price,})
    if request.method == 'POST':
        period=request.POST.get('period')
        if sub_type=='trial' or plan.name=='Free':
            return redirect('subs:payment_success', plan_id, school_id, sub_type, period)
        else:
            data=initiate_payment(request, plan_id, school_id, sub_type, period)
            d=SubscriptionPayments()
            d.school=school
            d.duration=data['duration']
            d.amount=data['price']
            d.trans_id=int(data['trans_id'])
            return redirect(data['checkout_url'])
    cont={'plan': plan, 'institution': school, 'school_id':school_id, 'sub':sub}
    return render(request, 'templates/subscription/subscribe.html', cont)

# View for subscription confirmation page
def subscription_success(request, plan_id, school_id, sub_type):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    school = get_object_or_404(School, id=school_id)  
    d=get_object_or_404(SubscriptionPayments, school=school)
    d.successful=True
    d.save()
    sub=sub_type
    if sub=='trial':pass 
    else: 
        sub=None
    cont={
        'plan': plan, 'institution': school, 'school_id':school_id, 'sub':sub
    }
    return render(request, 'templates/subscription/success.html', cont)


@login_required
def subscription(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if is_admin(request) == False: return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    sub=SchoolSubscription.objects.get(school=institution)
    cont={
        'institution':institution,
        'school_id':school_id,
        'sub':sub
    }
    return render(request, 'templates/subscription/subscription.html', cont)