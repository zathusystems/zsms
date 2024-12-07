# Generated by Django 5.1 on 2024-08-11 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooladminstration', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='courses',
            field=models.ManyToManyField(blank=True, default=False, related_name='enrollement', to='schooladminstration.course'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='subjects',
            field=models.ManyToManyField(blank=True, default=False, related_name='enrollement', to='schooladminstration.subject'),
        ),
    ]
