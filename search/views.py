# from unicodedata import category
from django.shortcuts import render
# from rest_framework import viewsets, filters

# from admins.models import VendorCategory
# from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
# from product.models import Product, ProductBrand, Category
# from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# # Create your views here.
# from vendor.models import Vendor
# #from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.core.paginator import Paginator, InvalidPage, EmptyPage
from main.utils import get_institution
from search import search
# from django.conf import settings

def results(request, school_id):
    # get current search phrase
    institution=get_institution(request, school_id)
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
   
    # get current page number. Set to 1 is missing or invalid
    # try:
    #     page = int(request.GET.get('page', 1))
    # except ValueError:
    #     page = 1
    # retrieve the matching products
    # vcategory='All'
    # if category=='students':
    #     vcategory = VendorCategory.objects.get(id=category_id)
    # elif category=='teachers':
    #     pass
    # elif category=='emiployees':
    #     pass

    results = search.search(q, category, school_id)
    # print(matching, 'matching bbbbbbbbbbbbbbbbbbbbbbbbb')
    # # generate the pagintor object
    # paginator = Paginator(matching,
    # settings.PRODUCTS_PER_PAGE)
    # try:
    #     results = paginator.page(page).object_list
    # except (InvalidPage, EmptyPage):
    #     results = paginator.page(1).object_list
    # # store the search
    # search.store(request, q)
    # print(q)
    # # the usual…
    # print(results, 'results lllllllllllllllllllllllll')
    page_title = 'Search Results for: ' + q + ' in ' + category
    # print(matching.count(), 'total matching data')
    cont={
       'school_id':school_id,
       'page_title':page_title,
       'results':results,
       'q':q,
       'search_category':category,
       'institution':institution
    }
    return render(request,  "templates/main/results.html", cont)


# def vendor_results(request, vendor_slug, vendor_id):
#     # get current search phrase
#     vendor=Vendor.objects.get(id=vendor_id)
#     template_name="vendor_store/vendor_search_result.html"
#     q = request.GET.get('q', '')
#     # get current page number. Set to 1 is missing or invalid
#     # try:
#     #     page = int(request.GET.get('page', 1))
#     # except ValueError:
#     #     page = 1
#     # retrieve the matching products
#     matching = search.VendorProducts(q, vendor_id).get('products')
#     matching = matching.filter(vendor=vendor)
#     # print(matching, 'matching bbbbbbbbbbbbbbbbbbbbbbbbb')
#     # # generate the pagintor object
#     # paginator = Paginator(matching,
#     # settings.PRODUCTS_PER_PAGE)
#     # try:
#     #     results = paginator.page(page).object_list
#     # except (InvalidPage, EmptyPage):
#     #     results = paginator.page(1).object_list
#     # # store the search
#     # search.store(request, q)
#     # print(q)
#     # # the usual…
#     # print(results, 'results lllllllllllllllllllllllll')
#     page_title = 'Search Results for: ' + q
#     print(matching.count(), 'total matching data')
#     cont={
#        'data':matching[:2],
#        'page_title':page_title,
#        'total_data':matching.count(),
#        'vendor':vendor,
#        'q':q,
#     }
#     return render(request, template_name, cont)



# class ProductViewSet(viewsets.ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['title', 'description', 'categories']
#     search_fields=['title', 'description', 'categories__category_title', 'vendor__name', 'brand__brand_title']
#     ordering_fields='__all__'

# class CategoryViewSet(viewsets.ModelViewSet):
#     serializer_class = CategorySerializer
#     queryset = Category.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['category_title']
#     search_fields=['category_title']
#     ordering_fields='__all__'

# class BrandViewSet(viewsets.ModelViewSet):
#     serializer_class = BrandSerializer
#     queryset = ProductBrand.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['brand_title']
#     search_fields=['brand_title']
#     ordering_fields='__all__'