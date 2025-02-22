# Generated by Django 5.1.1 on 2024-10-09 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_admin', '0002_remove_systemfeature_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('phone', models.IntegerField(max_length=15)),
                ('message', models.TextField()),
                ('icon', models.ImageField(blank=True, null=True, upload_to='features/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
