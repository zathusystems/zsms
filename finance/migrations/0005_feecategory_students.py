# Generated by Django 5.1 on 2024-08-14 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_remove_feepayment_fully_paid_feecategory_description_and_more'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='feecategory',
            name='students',
            field=models.ManyToManyField(related_name='fee_category', to='student.student'),
        ),
    ]
