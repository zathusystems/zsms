# Generated by Django 5.1 on 2024-08-19 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_calendar', '0007_alter_academicyear_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='year',
            field=models.CharField(help_text='e.g 2024-2025', max_length=9),
        ),
    ]
