# Generated by Django 5.1 on 2024-08-14 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_feecategory_students'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feecategory',
            name='students',
        ),
        migrations.AddField(
            model_name='feecategory',
            name='enrollment',
            field=models.ManyToManyField(related_name='fee_category', to='student.enrollment'),
        ),
    ]
