# Generated by Django 5.1 on 2024-08-18 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_expense_academic_year_expense_term_and_more'),
        ('school_calendar', '0005_alter_academicyear_options_term_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='academic_year',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payroll', to='school_calendar.academicyear'),
        ),
        migrations.AddField(
            model_name='payroll',
            name='term',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payroll', to='school_calendar.term'),
        ),
    ]
