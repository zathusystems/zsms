from django.db import models
from django.utils import timezone
from schooladminstration.models import Institution
from datetime import datetime, date

# Create your models here.
class AcademicYear(models.Model):
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='academic_year')
    year=models.CharField(max_length=9, help_text='e.g 2024-2025')
    start_date=models.DateField(help_text='starting date of this academic year')
    end_date=models.DateField(help_text='ending date of this academic year')
    date=models.DateField(auto_now_add=True)
    closed=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.year}'
    
class Term(models.Model):
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='terms')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    title=models.CharField(max_length=50, help_text='e.g Term 1/Semister 2')
    start_date=models.DateField(help_text='starting date of this term/semister')
    end_date=models.DateField(help_text='ending date of this Term/Semister')
    date=models.DateField(auto_now_add=True)
    closed=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title}'

class CalendarEvent(models.Model):
    EVENT_TYPES = [
        ('holiday', 'Holiday'),
        ('exam', 'Exam'),
        ('meeting', 'Meeting'),
        ('event', 'Event'),
    ]
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-start_date']
    def __str__(self):
        return f'{self.title}'
    def is_ongoing(self):
        if datetime.today().date() > self.start_date and datetime.today().date() < self.end_date:
            return True
    def remaining_day(self):
        d=(self.start_date - datetime.today().date()).days
        return d
    def passed_day(self):
        return datetime.today().date() > self.end_date