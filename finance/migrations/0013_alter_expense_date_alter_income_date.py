# Generated by Django 5.1 on 2024-08-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_alter_fee_options_alter_feepayment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
