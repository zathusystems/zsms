# Generated by Django 5.1 on 2024-08-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_calendar', '0004_alter_academicyear_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicyear',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='term',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
