from django.db import models
from student.models import Student
from django.contrib.auth import get_user_model
from schooladminstration.models import Institution
# Create your models here.
class Parent(models.Model):
    u=get_user_model()
    t=(
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr')
    )
    title=models.CharField(max_length=50, null=True, blank=True, default=None, choices=t)
    user=models.ForeignKey(u, on_delete=models.CASCADE, related_name='parent')
    first_name=models.CharField(max_length=50, null=True, blank=True, default=None)
    last_name=models.CharField(max_length=50, null=True, blank=True, default=None)
    address=models.CharField(max_length=100)
    phone=models.IntegerField()
    sex=(
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender=models.CharField(max_length=10, choices=sex)
    children=models.ManyToManyField(Student, related_name='parent', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.first_name
    
class ParentDetails(models.Model):
    t=(
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr')
    )
    title=models.CharField(max_length=50, null=True, blank=True, default=None, choices=t)
    first_name=models.CharField(max_length=50, null=True, blank=True, default=None)
    last_name=models.CharField(max_length=50, null=True, blank=True, default=None)
    address=models.CharField(max_length=100)
    phone=models.IntegerField()
    sex=(
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender=models.CharField(max_length=10, choices=sex)
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parent_details', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.first_name
    
class ParentStudentAccess(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='parent_access')
    parent=models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='parent_access')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parent_access', null=True, blank=True)
    approved=models.BooleanField(default=False)
    def __str__(self):
        return self.school.institution_name