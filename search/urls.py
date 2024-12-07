from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

app_name='search'
urlpatterns = [
    path('search-results-<uuid:school_id>/', results, name='search'),
]

# router = DefaultRouter()
# router.register('api/products', ProductViewSet, basename='products')
# router.register('api/categories', CategoryViewSet, basename='categories')
# router.register('api/brands', BrandViewSet, basename='brands')

# urlpatterns += router.urls