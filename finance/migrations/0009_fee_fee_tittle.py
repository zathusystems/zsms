# Generated by Django 5.1 on 2024-08-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_fee_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='fee_tittle',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
