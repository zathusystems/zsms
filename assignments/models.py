from django.db import models
from django.utils import timezone
from classroom.models import ClassRoom
from schooladminstration.models import Course, Institution, Subject
from student.models import Student
from teacher.models import Instructor

# Create your models here.
class Assignment(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='assignments', default=None, null=True, blank=True)
    teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='assignments')
    classi = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, default=None)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, default=None)
    cates=(
        ('test', 'Test/Mid Exams'),
        ('assignment', 'Assignment/home work')
    )
    title = models.CharField(max_length=50, choices=cates)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    total_marks=models.IntegerField(max_length=3, default=None)
    due_date = models.DateField()
    def __str__(self):
        return self.title
    
    def highest(self):
        
        d= self.ass_results.all()
        li=[]
        for marks in d:
            li.append(marks.marks)
        if len(li) > 0:
            return max(li)
        return ''
    
    def lowest(self):
        d= self.ass_results.all()
        li=[]
        for marks in d:
            li.append(marks.marks)
        if len(li) > 0:
            return min(li)
        return ''
    
    def students_attended(self):
        d= self.ass_results.all()
        li=[]
        for data in d:
            li.append(data.student)
        if len(li) > 0:
            return li
        return None

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='ass_results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ass_results')
    submission_date = models.DateField(auto_now_add=True)
    # file = models.FileField(upload_to='submissions/')
    marks = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together=['student', 'assignment']

    def __str__(self):
        return f"{self.assignment.title} - {self.student.first_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Additional logic if needed (e.g., update average grade)

    


class ClassWork(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='class_works')
    teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='class_works')
    classi = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='class_works')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, default=None)
    date = models.DateField(auto_now_add=True)
    number_of_questions = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.title} class work"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Additional logic if needed (e.g., update average grade)

class ClassWorkResult(models.Model):
    class_work = models.ForeignKey(ClassWork, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    date = models.DateField(auto_now_add=True)
    marks = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together=['student', 'class_work']

    def __str__(self):
        return f"{self.student.first_name} - {self.student.last_name} class work result"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Additional logic if needed (e.g., update average grade)