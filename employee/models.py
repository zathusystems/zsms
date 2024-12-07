from django.db import models
from schooladminstration.models import Institution
from teacher.models import Instructor
from django.utils import timezone
# Create your models here.

class Employee(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='employees')
    teacher=models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, related_name='employee', null=True, blank=True, default=None)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    sex=(
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender=models.CharField(max_length=10, choices=sex)
    date_of_birth=models.DateField(null=True, blank=True, default=None)
    phone=models.IntegerField(null=True, blank=True, default=None)
    address=models.TextField(null=True, blank=True, default=None)
    position=models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    date_of_hire = models.DateField(null=True, blank=True, default=None)

    EMPLOYMENT_STATUS = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('CON', 'Contract'),
        ('SUB', 'Substitute'),
    ]
    employment_status = models.CharField(max_length=3, choices=EMPLOYMENT_STATUS, default=None, blank=True, null=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.position}'
    
    def needs_attention(self):
        fields=[self.address, self.salary, self.date_of_hire, self.date_of_birth, self.employment_status]
        if None in fields:
            return True
        return False

class Document(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='employee_documents')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    DOC_TYPE = [
        ('CV', 'cv'),
        ('Identification Card', 'identification card'),
        ('Contract', 'contract'),
        ('Certification', 'certification'),
        ('Other', 'other'),
    ]
    doc_type = models.CharField(max_length=100, choices=DOC_TYPE)  # e.g., contract, ID, certification
    document = models.FileField(upload_to='school_files/employee_documents/')
    def __str__(self):
        return f"{self.doc_type} - {self.employee.first_name, self.employee.last_name}"
    
class AttendanceDate(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='employee_attendance_dates')
    date = models.DateField(default=timezone.now, unique=True)
    def employees_attended(self):
        atte=self
        n=atte.employee_attendance.filter(status='present')
        return n.count()

    def employees_absent(self):
        atte=self
        n=atte.employee_attendance.filter(status='absent')
        return n.count()
    
    def employees_late(self):
        atte=self
        n=atte.employee_attendance.filter(status='late')
        return n.count()

class EmployeeAttendance(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='employee_attendance')
    attendance_date=models.ForeignKey(AttendanceDate, on_delete=models.CASCADE, related_name='employee_attendance', default=None, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])
    processed=models.BooleanField(default=False)


class LeaveRequest(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='leaves')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_status = models.CharField(max_length=20, default=None, choices=[('sick', 'Sick'), ('vacation', 'Vacation'), ('personal', 'Personal')])
    leave_type = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])
    start_date = models.DateField()
    end_date = models.DateField(default=None, null=True, blank=True)
    status = models.CharField(max_length=10, default='Approved', choices=[('Pending', 'Pending'), ('Approved', 'Approved'),  ('Rejected', 'Rejected'), ('Returned', 'Returned')])
    processed=models.BooleanField(default=False)
    date_returned=models.DateField(default=None, null=True, blank=True)
    def total_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 'unknown'
    