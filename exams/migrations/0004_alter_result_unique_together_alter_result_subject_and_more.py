# Generated by Django 5.1.1 on 2024-10-10 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_result_academic_year_result_term'),
        ('school_calendar', '0009_calendarevent'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='result',
            name='subject',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_results', to='exams.examsubjects'),
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together={('student', 'subject', 'term')},
        ),
    ]
