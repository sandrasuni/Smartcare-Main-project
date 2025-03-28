# Generated by Django 5.1.5 on 2025-02-07 06:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.IntegerField(choices=[(1, 'Admin'), (2, 'Doctor'), (3, 'Pharmacist'), (4, 'Public Health Nurse'), (5, 'ASHA Worker'), (6, 'User (Patient)'), (7, 'Junior Health Inspector'), (8, 'Health Care')])),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HealthCareProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_name', models.CharField(max_length=255)),
                ('h_email', models.EmailField(max_length=254, unique=True)),
                ('h_phone', models.CharField(max_length=15, unique=True)),
                ('h_year_of_experience', models.PositiveIntegerField(default=0)),
                ('admin_approve', models.BooleanField(default=False)),
                ('h_type', models.CharField(choices=[('fhc', 'FHC'), ('chc', 'CHC'), ('phc', 'PHC')], max_length=3)),
                ('h_location', models.CharField(max_length=255)),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('medical_registration_number', models.CharField(max_length=100)),
                ('specialization', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('years_of_experience', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('health_centre_status', models.BooleanField(default=False)),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fk_healthcare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.healthcareprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ASHAWorkerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('asha_worker_id', models.CharField(max_length=100)),
                ('community_assigned', models.TextField()),
                ('training_details', models.TextField()),
                ('experience_in_health_awareness', models.TextField()),
                ('address', models.TextField()),
                ('health_centre_status', models.BooleanField(default=False)),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fk_healthcare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.healthcareprofile')),
            ],
        ),
        migrations.CreateModel(
            name='JuniorHealthInspectorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('inspection_license_number', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('experience_in_health_inspection', models.TextField()),
                ('address', models.TextField()),
                ('health_centre_status', models.BooleanField(default=False)),
                ('fk_healthcare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.healthcareprofile')),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('emergency_contact', models.CharField(max_length=15)),
                ('patient_id', models.CharField(blank=True, max_length=15, unique=True)),
                ('status', models.BooleanField(default=False)),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('s_continuous_medication', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='reports/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fk_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.patientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='PharmacistProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('pharmacy_registration_number', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('years_of_experience', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('health_centre_status', models.BooleanField(default=False)),
                ('fk_healthcare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.healthcareprofile')),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicHealthNurseProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('nursing_license_number', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('years_of_experience', models.PositiveIntegerField()),
                ('training_in_public_health', models.TextField()),
                ('address', models.TextField()),
                ('health_centre_status', models.BooleanField(default=False)),
                ('fk_healthcare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.healthcareprofile')),
                ('fk_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
