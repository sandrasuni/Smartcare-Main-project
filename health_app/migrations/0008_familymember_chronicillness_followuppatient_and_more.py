# Generated by Django 5.1.6 on 2025-03-06 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0007_jhiimgprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChronicIllness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illness', models.CharField(max_length=255)),
                ('medications_prescribed', models.TextField()),
                ('following_medication', models.BooleanField(default=False)),
                ('family_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chronic_illnesses', to='health_app.familymember')),
            ],
        ),
        migrations.CreateModel(
            name='FollowUpPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=255)),
                ('last_checkup_date', models.DateField()),
                ('next_followup_date', models.DateField()),
                ('family_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_ups', to='health_app.familymember')),
            ],
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_of_household', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(max_length=15)),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HealthEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrition', models.BooleanField(default=False)),
                ('breastfeeding', models.BooleanField(default=False)),
                ('family_planning', models.BooleanField(default=False)),
                ('sanitation_hygiene', models.BooleanField(default=False)),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_education', to='health_app.household')),
            ],
        ),
        migrations.AddField(
            model_name='familymember',
            name='household',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='health_app.household'),
        ),
        migrations.CreateModel(
            name='EmergencyReferral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('critical_health_issue', models.BooleanField(default=False)),
                ('referred_to_health_center', models.BooleanField(default=False)),
                ('referral_details', models.TextField(blank=True, null=True)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_cases', to='health_app.household')),
            ],
        ),
        migrations.CreateModel(
            name='ChildHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_name', models.CharField(blank=True, max_length=255, null=True)),
                ('child_age', models.IntegerField(blank=True, null=True)),
                ('birth_weight', models.FloatField(blank=True, null=True)),
                ('immunization_status', models.TextField(blank=True, null=True)),
                ('nutritional_status', models.CharField(blank=True, choices=[('Normal', 'Normal'), ('Underweight', 'Underweight')], max_length=50, null=True)),
                ('vaccination_done', models.BooleanField(default=False)),
                ('vaccination_due_date', models.DateField(blank=True, null=True)),
                ('family_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_health', to='health_app.household')),
            ],
        ),
        migrations.CreateModel(
            name='PregnantWoman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('expected_delivery_date', models.DateField(blank=True, null=True)),
                ('antenatal_checkups_completed', models.BooleanField(default=False)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pregnancy_details', to='health_app.household')),
            ],
        ),
        migrations.CreateModel(
            name='SanitationHygiene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_toilet', models.BooleanField(default=False)),
                ('has_clean_drinking_water', models.BooleanField(default=False)),
                ('has_handwashing_facility', models.BooleanField(default=False)),
                ('household', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sanitation_hygiene', to='health_app.household')),
            ],
        ),
        migrations.CreateModel(
            name='VisitDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('reason_for_visit', models.TextField()),
                ('symptoms_reported', models.TextField(blank=True, null=True)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='health_app.household')),
            ],
        ),
    ]
