# Generated by Django 5.1.6 on 2025-03-10 17:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0015_pharmacistimgprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bedridden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('existing_conditions', models.TextField(blank=True)),
                ('current_medications', models.TextField(blank=True)),
                ('allergies', models.TextField(blank=True)),
                ('past_surgeries', models.TextField(blank=True)),
                ('duration_of_bedridden', models.CharField(max_length=100)),
                ('primary_diagnosis', models.CharField(max_length=100)),
                ('level_of_dependency', models.CharField(choices=[('Partial', 'Partial'), ('Complete', 'Complete')], max_length=10)),
                ('caregiver_name', models.CharField(max_length=100)),
                ('caregiver_contact', models.CharField(max_length=15)),
                ('date_of_registration', models.DateField(auto_now_add=True)),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
