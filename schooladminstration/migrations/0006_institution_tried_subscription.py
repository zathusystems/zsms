# Generated by Django 5.1.1 on 2024-09-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooladminstration', '0005_alter_institution_edu_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='tried_subscription',
            field=models.BooleanField(default=False),
        ),
    ]
