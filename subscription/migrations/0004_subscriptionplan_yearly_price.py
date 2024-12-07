# Generated by Django 5.1.1 on 2024-09-20 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_alter_subscriptionplan_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='yearly_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
    ]
