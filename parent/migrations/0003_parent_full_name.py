# Generated by Django 5.1.1 on 2024-11-30 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parent', '0002_parentstudentaccess_delete_studentparents'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='full_name',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
