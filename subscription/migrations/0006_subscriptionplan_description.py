# Generated by Django 5.1.1 on 2024-09-28 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_feature_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
