from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
import uuid
# Create your models here.
#-------- institution models -----------#
#---------------------------------------#
class Institution(models.Model):
    institution_name=models.CharField(max_length=50)
    id=models.CharField(primary_key=True, max_length=100, blank=True, unique=True, default=uuid.uuid4)
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='institution', blank=True, null=True, default=None)
    name_of_head=models.CharField(max_length=50, null=True, blank=True, default=None)
    name_of_principal=models.CharField(max_length=50, null=True, blank=True, default=None)
    name_of_registrar=models.CharField(max_length=50, null=True, blank=True, default=None)
    phone=models.CharField(max_length=50, null=True, blank=True)
    country=models.CharField(max_length=50, null=True, blank=True)
    city=models.CharField(max_length=50, null=True, blank=True)
    tried_subscription=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    edu=(
        ('primary education', 'Primary Education'),
        ('secondary education', 'Secondary Education'),
        ('tertialy education', 'Tertiary Education'),
    )
    edu_offer=models.CharField(max_length=20, choices=edu)
    def __str__(self):
        return self.institution_name

class SchoolAddress(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='contact_details')
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State/Province")
    country = models.CharField(max_length=100, verbose_name="Country")
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email Address")

    def __str__(self):
        return self.school.institution_name


#---------- acadamic models ------------#
#---------------------------------------#
class Department(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='departments')
    title=models.CharField(max_length=50, null=True, blank=True)
    description=models.TextField()
    #head_od=models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='head_of_d')
    edu=(
        ('secondary education', 'Secondary Education'),
        ('tertialy education', 'Tertialy Education')
    )
    is_for=models.CharField(max_length=20, choices=edu)
    def __str__(self):
        return self.title

class Course(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='courses')
    title=models.CharField(max_length=30, null=True, blank=True)
    description=models.TextField()
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
 
    def __str__(self):
        return self.title
        
class Subject(models.Model):
    title=models.CharField(max_length=30, null=True, blank=True)
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='subjects')
    description=models.TextField()
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True, default=None)
    edu=(
        ('secondary education', 'Secondary Education'),
        ('tertialy education', 'Tertialy Education')
    )
    is_for=models.CharField(max_length=20, choices=edu)

    def __str__(self):
        return self.title

class Logo(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='logo')
    logo = models.ImageField(upload_to='school_files/logo')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.school.institution_name
