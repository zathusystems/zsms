# Generated by Django 5.1.1 on 2024-11-30 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_remove_submission_assignment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='title',
            field=models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Dr', 'Dr')], default=None, max_length=50, null=True),
        ),
    ]
