# Generated by Django 5.1.1 on 2024-10-20 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0005_alter_submission_assignment_alter_submission_student'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classworkresult',
            unique_together={('student', 'class_work')},
        ),
        migrations.AlterUniqueTogether(
            name='submission',
            unique_together={('student', 'assignment')},
        ),
    ]
