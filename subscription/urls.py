from django.urls import path
from . import views
app_name='subs'
urlpatterns = [
    path('subscriptions-<uuid:school_id>/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/<int:plan_id>-<uuid:school_id>/<slug:sub_type>/', views.subscribe_to_plan, name='subscribe_to_plan'),
    path('subscription-success/<int:plan_id>-<uuid:school_id>/<slug:sub_type>/', views.subscription_success, name='sub_success'),
    path('payment-success/<int:plan_id>-<uuid:school_id>-<slug:sub_type>-<slug:period>', views.after_payment_success, name='payment_success'),
    path('subscription-<uuid:school_id>/', views.subscription, name='subs'),
    path('upgrade-subscription-<uuid:school_id>/', views.upgrade, name='upgrade'),
    path('expired-subscription-<uuid:school_id>/', views.expired, name='expired'),
]
