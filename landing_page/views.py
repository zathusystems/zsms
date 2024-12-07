from django.shortcuts import render
from subscription.models import SubscriptionPlan, Feature
from system_admin.models import About, Faqs, Privacy, SystemFeature, Contact, Terms
# Create your views here.
def index(request):
    plans=SubscriptionPlan.objects.all()
    features=Feature.objects.all()
    system_features=SystemFeature.objects.all()
    about=About.objects.first()
    cont={
        'plans':plans,
        'features':features,
        'system_features':system_features,
        'about':about
    }
    return render(request, 'templates/landing_page/index.html', cont)

def system_features(request):
    system_features=SystemFeature.objects.all()
    cont={
        'system_features':system_features
    }
    return render(request, 'templates/landing_page/features.html', cont)

def system_feature(request, f_id):
    feature=SystemFeature.objects.get(id=f_id)
    features=SystemFeature.objects.all()
    cont={
        'feature':feature,
        'features':features
    }
    return render(request, 'templates/landing_page/feature.html', cont)

def pricing(request):
    plans=SubscriptionPlan.objects.all()
    features=Feature.objects.all()
    cont={
        'plans':plans,
        'features':features,
    }
    return render(request, 'templates/landing_page/pricing.html', cont)

def contact_us(request):
    if request.method=='POST':
        name=request.POST.get('full_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        d=Contact()
        d.name=name
        d.email=email
        d.phone=phone
        d.message=message
        d.save()
        return render(request, 'templates/landing_page/thank_you.html')
    cont={
       
    }
    return render(request, 'templates/landing_page/contact_us.html', cont)

def about(request):
    about=About.objects.first()
    cont={
       'about':about
    }
    return render(request, 'templates/landing_page/about.html', cont)

def terms(request):
    terms=Terms.objects.first()
    cont={
       'terms':terms
    }
    return render(request, 'templates/landing_page/terms.html', cont)

def privacy(request):
    privacy=Privacy.objects.first()
    cont={
       'privacy':privacy
    }
    return render(request, 'templates/landing_page/privacy.html', cont)

def faqs(request):
    faqs=Faqs.objects.first()
    cont={
       'faqs':faqs
    }
    return render(request, 'templates/landing_page/faqs.html', cont)