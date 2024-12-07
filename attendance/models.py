from django.db import models
from django.contrib.auth import get_user_model

from student.models import Student
from classroom.models import ClassRoom
from schooladminstration.models import Institution, Subject, Course

class StudentAttendance(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='attendance', null=True, blank=True, default=None)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance', null=True, blank=True, default=None)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance', null=True, blank=True, default=None)
    class_room=models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='attendance', null=True, blank=True, default=None)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def students_attended(self):
        atte=StudentAttendance.objects.get(id=self.id)
        n=atte.attendance_status.filter(status='attended')
        return n.count()

    def students_absent(self):
        atte=StudentAttendance.objects.get(id=self.id)
        n=atte.attendance_status.filter(status='absent')
        return n.count()
    
    def students_late(self):
        atte=StudentAttendance.objects.get(id=self.id)
        n=atte.attendance_status.filter(status='late')
        return n.count()

class StudentAttendanceStatus(models.Model):
    attendance=models.ForeignKey(StudentAttendance, on_delete=models.CASCADE, related_name='attendance_status')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_status')
    date=models.DateTimeField(auto_now_add=True)
    s=(
        ('attended', 'Attended'),
        ('absent', 'Absent'),
        ('late', 'Late')
    )
    status=models.CharField(max_length=10, choices=s)
    reason=models.TextField(null=True, blank=True, default=None)