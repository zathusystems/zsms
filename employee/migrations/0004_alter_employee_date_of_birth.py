# Generated by Django 5.1 on 2024-09-08 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_alter_employee_address_alter_employee_date_of_hire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_of_birth',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
