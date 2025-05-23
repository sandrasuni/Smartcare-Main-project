# Generated by Django 5.1.6 on 2025-03-07 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0009_healthsurvey'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaternalCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('household_name', models.CharField(blank=True, max_length=100, null=True)),
                ('pregnant_member_name', models.CharField(blank=True, max_length=100, null=True)),
                ('expected_delivery_date', models.DateField(blank=True, null=True)),
                ('antenatal_checkups', models.BooleanField(default=False)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('husband_name', models.CharField(blank=True, max_length=100, null=True)),
                ('husband_contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('last_menstrual_period', models.DateField(blank=True, null=True)),
                ('gestational_age_weeks', models.PositiveIntegerField(blank=True, null=True)),
                ('pregnancy_risk_factor', models.CharField(blank=True, choices=[('High', 'High'), ('Moderate', 'Moderate'), ('Low', 'Low')], max_length=10, null=True)),
                ('number_of_pregnancies', models.PositiveIntegerField(blank=True, null=True)),
                ('number_of_live_births', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
    ]
