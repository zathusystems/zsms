# Generated by Django 5.1.1 on 2024-09-21 11:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schooladminstration', '0005_alter_institution_edu_offer'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('children', models.ManyToManyField(blank=True, null=True, related_name='parent', to='student.student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='studentParents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='parent.parent')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='schooladminstration.institution')),
            ],
        ),
    ]
