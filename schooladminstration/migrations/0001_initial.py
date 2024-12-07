# Generated by Django 5.0.7 on 2024-08-04 15:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField()),
                ('is_for', models.CharField(choices=[('secondary education', 'Secondary Education'), ('tertialy education', 'Tertialy Education')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='schooladminstration.department')),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_name', models.CharField(max_length=50)),
                ('name_of_head', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('name_of_principal', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('name_of_registrar', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('edu_offer', models.CharField(choices=[('secondary education', 'Secondary Education'), ('tertialy education', 'Tertiary Education')], max_length=20)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institution', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField()),
                ('is_for', models.CharField(choices=[('secondary education', 'Secondary Education'), ('tertialy education', 'Tertialy Education')], max_length=20)),
                ('course', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='schooladminstration.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='schooladminstration.department')),
            ],
        ),
    ]
