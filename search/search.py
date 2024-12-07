from student.models import Student
from teacher.models import Instructor
from employee.models import Employee
from library.models import Book
from django.db.models import Q

STRIP_WORDS = ['a','an','and','by','for','from','in','no','not',
'of','on','or','that','the','to','with']
# store the search text in the database

def search(text, category, school_id):
    words = _prepare_words(text)
    if category=='students':
        students=Student.objects.filter(school__id=school_id)
        results = {}
        results['students'] = []
        for word in words:
            students = students.filter(
                Q(first_name__icontains=word) |
                Q(last_name__icontains=word) | 
                Q(phone__icontains=word) |
                Q(address__icontains=word) |
                Q(id_number__icontains=word) |
                Q(gender__icontains=word)
            )
        results['students'] = students
        return results
    if category=='teachers':
        teachers=Instructor.objects.filter(school__id=school_id)
        results = {}
        results['teachers'] = []
        for word in words:
            teachers = teachers.filter(
                Q(first_name__icontains=word) |
                Q(last_name__icontains=word) | 
                Q(phone__icontains=word) |
                Q(department__title__icontains=word) |
                Q(gender__icontains=word)
            )
        results['teachers'] = teachers
        return results
    if category=='employees':
        employees=Employee.objects.filter(school__id=school_id)
        results = {}
        results['employees'] = []
        for word in words:
            employees = employees.filter(
                Q(first_name__icontains=word) |
                Q(last_name__icontains=word) | 
                Q(phone__icontains=word) |
                Q(address__icontains=word) |
                Q(position__icontains=word) |
                Q(gender__icontains=word)
            )
        results['employees'] = employees
        return results
    if category=='books':
        books=Book.objects.filter(school__id=school_id)
        results = {}
        results['books'] = []
        for word in words:
            books = books.filter(
                Q(title__icontains=word) |
                Q(author__icontains=word) | 
                Q(isbn__icontains=word) |
                Q(description__icontains=word)
            )
        results['books'] = books
        return results

# def store(request, q):
#     # if search term is at least three chars long, store in db
#     if len(q) > 2:
#         term = SearchTerm()
#         term.q = q
#         term.ip_address = request.META.get('REMOTE_ADDR')
#         term.user = None
#         if request.user.is_authenticated:
#             term.user = request.user
#             term.save()
# # get products matching the search text
# def products(search_text, category_id):
#     words = _prepare_words(search_text)
#     products = Product.objects.all()
#     if category_id:
#         products=products.filter(vendor__vendortype=category_id)
        
#     results = {}
#     results['products'] = []
#     # iterate through keywords
#     for word in words:
#         products = products.filter(
#             Q(vendor__vendortype__name__icontains=word) |
#             Q(title__icontains=word) | 
#             Q(description__icontains=word) |
#             Q(categories__category_title__icontains=word) |
#             Q(brand__brand_title__icontains=word) |
#             Q(is_for__icontains=word)
#         )
#     results['products'] = products
#     return results

# def VendorProducts(search_text, vendor_id):
#     vendor=Vendor.objects.get(id=vendor_id)
#     words = _prepare_words(search_text)
#     products = Product.objects.all()
#     products=products.filter(vendor=vendor)
        
#     results = {}
#     results['products'] = []
#     # iterate through keywords
#     for word in words:
#         products = products.filter(
#             Q(vendor__vendortype__name__icontains=word) |
#             Q(title__icontains=word) | 
#             Q(description__icontains=word) |
#             Q(categories__category_title__icontains=word) |
#             Q(brand__brand_title__icontains=word) |
#             Q(is_for__icontains=word)
#         )
#     results['products'] = products
#     return results
# strip out common words, limit to 5 words
def _prepare_words(search_text):
    words = search_text.split(' ')
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]