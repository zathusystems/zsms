# Generated by Django 5.1.1 on 2024-10-20 23:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0021_alter_advancepayroll_unique_together_and_more'),
        ('school_calendar', '0009_calendarevent'),
        ('schooladminstration', '0007_institution_created_at'),
        ('student', '0002_alter_enrollment_courses_alter_enrollment_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='period',
            field=models.CharField(blank=True, choices=[('once off', 'Once Off'), ('per month', 'Per Month'), ('per term', 'Per Term'), ('per semister', 'Per Semister'), ('per year', 'Per Year')], default='per term', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='feepayment',
            name='fully_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='OtherFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_title', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('period', models.CharField(choices=[('once off', 'Once Off'), ('per month', 'Per Month'), ('per term', 'Per Term'), ('per semister', 'Per Semister'), ('per year', 'Per Year')], max_length=20)),
                ('fee_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('closed', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('school', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_fees', to='schooladminstration.institution')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_discount', models.BooleanField(default=False)),
                ('discount_percentage', models.IntegerField(max_length=2)),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, default=False, max_digits=10, null=True)),
                ('academic_year', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='school_calendar.academicyear')),
                ('fee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='finance.fee')),
                ('school', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='schooladminstration.institution')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='student.student')),
                ('term', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='school_calendar.term')),
                ('other_fee', models.ManyToManyField(blank=True, default=None, null=True, related_name='invoices', to='finance.otherfee')),
            ],
        ),
        migrations.AddField(
            model_name='feepayment',
            name='other_fee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_fee_payments', to='finance.otherfee'),
        ),
    ]
