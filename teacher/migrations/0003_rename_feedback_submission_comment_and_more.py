# Generated by Django 5.1.1 on 2024-10-19 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_alter_instructor_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='feedback',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='grade',
            new_name='marks',
        ),
        migrations.AddField(
            model_name='assignment',
            name='total_marks',
            field=models.IntegerField(default=None, max_length=3),
        ),
    ]
