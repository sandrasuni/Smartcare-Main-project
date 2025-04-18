# Generated by Django 5.1.6 on 2025-03-07 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0010_maternalcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaternalVisitSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateField(blank=True, null=True)),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('visit_type', models.CharField(blank=True, choices=[('First Trimester', 'First Trimester'), ('Second Trimester', 'Second Trimester'), ('Third Trimester', 'Third Trimester'), ('Postnatal', 'Postnatal')], max_length=20, null=True)),
                ('visit_status', models.CharField(blank=True, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Missed', 'Missed')], max_length=10, null=True)),
                ('maternal_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_schedules', to='health_app.maternalcase')),
            ],
        ),
    ]
