from django.db import models

from classroom.models import ClassRoom
from schooladminstration.models import Institution, Subject

# Create your models here.
class TimeTable(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='titmetable')
    title=models.CharField(max_length=50, null=True, blank=True, default=None)
    classes=models.ManyToManyField(ClassRoom, null=True, blank=True, default=None , related_name='timetable')
    date_created=models.DateTimeField(auto_now_add=True)
    

class TimeTableSubjects(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='timetable_subjects')
    s=(
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday')
    )
    day=models.CharField(max_length=10, choices=s)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable', null=True, blank=True, default=False)
    start_time=models.TimeField()
    end_time=models.TimeField()
