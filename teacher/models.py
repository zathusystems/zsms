from datetime import datetime
from django.db import models
from schooladminstration.models import *
from django.utils import timezone

from student.models import *

# Create your models here.

#------------ staff models -------------#
#---------------------------------------#
class Instructor(models.Model):
    u=get_user_model()
    user=models.ForeignKey(u, on_delete=models.CASCADE, related_name='instructor_profile')
    t=(
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr')
    )
    title=models.CharField(max_length=50, null=True, blank=True, default=None, choices=t)
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='instructors')
    first_name=models.CharField(max_length=30, null=True, blank=True, default=None)
    last_name=models.CharField(max_length=30, null=True, blank=True, default=None)
    phone=models.IntegerField(null=True, blank=True, default=None)
    sex=(
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender=models.CharField(max_length=10, choices=sex)
    subjects_taught=models.ManyToManyField(Subject, related_name='instructor', blank=True, default=None)
    courses_taught=models.ManyToManyField(Course, related_name='instructor', blank=True, default=None)
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='instructors', null=True, blank=True, default=None)
    created_at=models.DateTimeField(auto_now_add=True)
    is_class_teacher=models.BooleanField(default=False)
    date_started=models.DateField(default=None, null=True, blank=True)
    approved=models.BooleanField(default=False)
    roles=(
        ('teacher', 'Teacher'),
        ('hr manager', 'Human Resource Manager'),
        ('librarian', 'Librarian'),
        ('finance manager', 'Finance Manager')
    )
    role=models.CharField(max_length=20, choices=roles, default=None, null=True, blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.approved:
            pass #create emiployee here

# class InstructorSchools(models.Model):
#     school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='instructors')
#     approved=models.BooleanField(default=False)
        
 
class LessonPlan(models.Model):
    title = models.CharField(max_length=200)
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='lessonplans', default=None, null=True, blank=True)
    description = models.TextField()
    objectives = models.TextField()
    materials_needed = models.TextField()
    content = models.TextField()
    date = models.DateField()
    teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    
# class Assignment(models.Model):
#     school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='assignments', default=None, null=True, blank=True)
#     teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE)
#     # classi = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, default=None)
#     Subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, default=None)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     created_at = models.DateTimeField(default=timezone.now)
#     total_marks=models.IntegerField(max_length=3, default=None)
#     due_date = models.DateField()
#     def __str__(self):
#         return self.title

# class Submission(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     submission_date = models.DateField(auto_now_add=True)
#     # file = models.FileField(upload_to='submissions/')
#     marks = models.FloatField(blank=True, null=True)
#     comment = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.assignment.title} - {self.student.first_name}"

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Additional logic if needed (e.g., update average grade)

class Gradebook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    average_grade = models.FloatField(default=0.0)
    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"

    def update_average(self):
        submissions = Submission.objects.filter(student=self.student, assignment__course=self.course)
        grades = [s.grade for s in submissions if s.grade is not None]
        if grades:
            self.average_grade = sum(grades) / len(grades)
            self.save()

    def generate_report_card(self):
        submissions = Submission.objects.filter(student=self.student, assignment__course=self.course)
        report_card = {
            'student': self.student.full_name,
            'course': self.course.title,
            'grades': [(s.assignment.title, s.grade, s.feedback) for s in submissions],
            'average_grade': self.average_grade,
        }
        return report_card
