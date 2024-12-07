from django.db import models
from datetime import date
from django.contrib.auth import get_user_model
from schooladminstration.models import Institution
from student.models import Student


# Create your models here.
# Model to represent a book
class Permision(models.Model):
    u=get_user_model()
    user=models.ForeignKey(u, on_delete=models.CASCADE, related_name='permissions')
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='permissions')
    is_supper_admin= models.BooleanField(default=False, blank=True)  # Title of the book
    is_admin= models.BooleanField(default=False, blank=True)  # Title of the book
    can_manage_employees = models.BooleanField(default=False, blank=True)  # Title of the book
    can_manage_finances = models.BooleanField(default=False, blank=True)  # Title of the book
    can_manage_library = models.BooleanField(default=False, blank=True)  # Title of the book
    date = models.DateField(auto_now_add=True) 
    def __str__(self):
        return f'Permissions for {self.user.first_name} {self.user.last_name}'