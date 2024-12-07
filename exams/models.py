from django.db import models
from classroom.models import ClassRoom
from school_calendar.models import AcademicYear, Term
from schooladminstration.models import Institution, Subject
from student.models import Student

class Exam(models.Model):
    title=models.CharField(max_length=50, null=True, default=None, blank=True, help_text='Give your exam time table a title. e.g (Form one Time table)')
    school=models.ForeignKey(Institution, related_name='exams', on_delete=models.CASCADE, null=True, default=None, blank=True)
    classes=models.ManyToManyField(ClassRoom, related_name='exams', null=True, blank=True)
    academic_year=models.ForeignKey(AcademicYear, related_name='exams', on_delete=models.CASCADE, null=True, default=None, blank=True)
    term=models.ForeignKey(Term, related_name='exams', on_delete=models.CASCADE, null=True, default=None, blank=True)
    def __str__(self):
        return f"{self.title} - {self.academic_year} - {self.term}"

class ExamDate(models.Model):
    school=models.ForeignKey(Institution, related_name='exam_date', on_delete=models.CASCADE, null=True, default=None, blank=True)
    exam=models.ForeignKey(Exam, related_name='exam_date', on_delete=models.CASCADE, null=True, default=None, blank=True)
    exam_date = models.DateField()
    date = models.DateField(auto_now_add=True, null=True, blank=True)  
    class Meta:
        ordering=['exam_date']

    def __str__(self):
        return f"{self.exam_date}"
    
class ExamSubjects(models.Model):
    exam_date=models.ForeignKey(ExamDate, related_name='exam_subjects', on_delete=models.CASCADE, null=True, default=None, blank=True)
    exam=models.ForeignKey(Exam, related_name='exam_subjects', on_delete=models.CASCADE, null=True, default=None, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_subjects')
    title=models.CharField(max_length=50)
    start_time=models.TimeField()
    end_time=models.TimeField()
    total_marks = models.PositiveIntegerField(default=100)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    class Meta:
        ordering=['start_time']
        unique_together = ('subject', 'title', 'exam_date')

    def __str__(self):
        return f"{self.subject.title} Exam on {self.exam_date}"

class Result(models.Model):
    school=models.ForeignKey(Institution, related_name='exam_results', on_delete=models.CASCADE, null=True, default=None, blank=True)
    subject = models.ForeignKey(ExamSubjects, on_delete=models.CASCADE, related_name='exam_results', null=True, default=None, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.PositiveIntegerField(max_length=3)
    academic_year=models.ForeignKey(AcademicYear, related_name='exam_results', on_delete=models.CASCADE, null=True, default=None, blank=True)
    term=models.ForeignKey(Term, related_name='exam_results', on_delete=models.CASCADE, null=True, default=None, blank=True)

    date = models.DateField(auto_now_add=True, null=True, blank=True)
    class Meta:
        unique_together = ('student', 'subject', 'term')

    def __str__(self):
        return f"{self.student} - {self.subject}"
    
    def highest(self):
        acd=self.subject.exam.academic_year
        trm=self.subject.exam.term
        d= Result.objects.filter(academic_year=acd, term=trm, id=self.pk)
        li=[]
        for marks in d:
            li.append(marks.marks_obtained)
        if len(li) > 0:
            return max(li)
        return ''
    def lowest(self):
        acd=self.subject.exam.academic_year
        trm=self.subject.exam.term
        d= Result.objects.filter(academic_year=acd, term=trm, id=self.pk)
        li=[]
        for marks in d:
            li.append(marks.marks_obtained)
        if len(li) > 0:
            return min(li)
        return ''
    
    def save(self, *args, **kwargs):
        self.academic_year = self.subject.exam.academic_year
        self.term=self.subject.exam.term
        super(Result, self).save(*args, **kwargs)


class ReportCard(models.Model):
    school=models.ForeignKey(Institution, related_name='report_cards', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    academic_year=models.ForeignKey(AcademicYear, related_name='report_cards', on_delete=models.CASCADE)
    term=models.ForeignKey(Term, related_name='report_cards', on_delete=models.CASCADE)
    exam=models.ForeignKey(Exam, related_name='report_cards', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report Card: {self.student} - {self.academic_year} ({self.term})"
