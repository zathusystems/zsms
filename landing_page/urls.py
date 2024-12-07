from django.urls import path
from .views import *
app_name='landing_page'

urlpatterns =[
    path('', index, name='landing'),
    # path('testimonials/', testimonials_view, name='testimonials'),
    path('pricing/', pricing, name='pricing'),
    path('features/', system_features, name='s_features'),
    path('features/feature-<int:f_id>/', system_feature, name='s_feature'),
    path('contact-us/', contact_us, name='contact'),
    path('About-us/', about, name='about'),
    path('fequent-asked-questions/', faqs, name='faqs'),
    path('terms-and-conditions/', terms, name='terms'),
    path('prpivacy-policy/', privacy, name='privacy'),
]
