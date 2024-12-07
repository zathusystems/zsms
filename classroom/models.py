from django.db import models

from schooladminstration.models import Institution
from student.models import Student
from teacher.models import Instructor

# Create your models here.
class ClassRoom(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='classes')
    class_name=models.CharField(max_length=20)
    students=models.ManyToManyField(Student, related_name='class_students', blank=True, default=None)
    # class_teacher=models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, related_name='classi', null=True, blank=True, default=None)
    teacher_assigned=models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, related_name='assigned_class', null=True, blank=True, default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['class_name']
        unique_together=['teacher_assigned', 'school']
        
    def __str__(self):
        return self.class_name
    
    def save(self, *args, **kwargs):
        if self.teacher_assigned is not None:
            self.teacher_assigned.is_class_teacher=True
            self.teacher_assigned.save()
            super(ClassRoom, self).save(*args, **kwargs)
