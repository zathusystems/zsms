# Generated by Django 5.1 on 2024-08-24 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
        ('schooladminstration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='school',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='schooladminstration.institution'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='school',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_checkouts', to='schooladminstration.institution'),
        ),
    ]
