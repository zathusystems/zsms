# Generated by Django 5.1.1 on 2024-10-09 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notice_posted_by_notification_sender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='audience',
            field=models.CharField(choices=[('all', 'All'), ('teachers', 'Teachers'), ('students', 'Students'), ('parents', 'Parents')], max_length=100),
        ),
    ]
