from django.db import models
# from finance.models import OtherFee
from schooladminstration.models import *
# Create your models here.
#----------- student models ------------#
#---------------------------------------#
class Student(models.Model):
    u=get_user_model()
    user=models.ForeignKey(u, on_delete=models.CASCADE, related_name='student_profile', blank=True, null=True, default=None)
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students')
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone=models.IntegerField(null=True, blank=True, default=None)
    address=models.CharField(max_length=100, null=True, blank=True, default=None)
    id_number=models.IntegerField(default=None)
    sex=(
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender=models.CharField(max_length=10, choices=sex)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        cls=self.class_students.first()
        cls=cls.class_name
        return f'{self.first_name} {self.last_name} - {cls}'
    
    def student_class_name(self):
        cls=self.class_students.first()
        cls=cls.class_name
        return cls
    
    def get_absolute_url(self):
        return ''

class Enrollment(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollement')
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='enrollement')
    courses=models.ManyToManyField(Course, related_name='enrollement', blank=True, default=False)
    subjects=models.ManyToManyField(Subject, related_name='enrollement', blank=True, default=False)
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='enrollement')
    start_date=models.DateField()
    s=(
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed')
    )
    status=models.CharField(max_length=10, choices=s, default='enrolled')
    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'
    
    def total_fee_paid(self):
        fee_cate=self.fee_category.get(enrollment=self)
        print(fee_cate, 'kkkkkkkkkkkkkk')
        fee=fee_cate.fees.filter(fee_category=fee_cate, closed=False).last()
        print(fee, 'kkkkkkkkkkkkkkkkkk')
        payments=self.student.fee_payments.filter(fee=fee)
        total=0
        for payment in payments:
            total+=payment.amount_paid
        return total
    
    def fee_balance(self):
        fee_cate=self.fee_category.get(enrollment=self)
        print(fee_cate, 'kkkkkkkkkkkkkk')
        fee=fee_cate.fees.filter(fee_category=fee_cate, closed=False).last()
        print(fee, 'kkkkkkkkkkkkkkkkkk')
        payments=self.student.fee_payments.filter(fee=fee)
        total=0
        for payment in payments:
            total+=payment.amount_paid
        return fee.fee_amount-total
