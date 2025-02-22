# Generated by Django 5.1.1 on 2024-10-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0027_alter_fee_unique_together'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherfee',
            name='enrollment',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='other_fees', to='student.enrollment'),
        ),
    ]
