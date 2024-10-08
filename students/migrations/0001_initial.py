# Generated by Django 5.0.7 on 2024-07-18 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parents', '0001_initial'),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uniqueNumber', models.CharField(max_length=50, unique=True)),
                ('admNumber', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('date_of_admission', models.DateField()),
                ('health_status', models.JSONField()),
                ('upi_number', models.CharField(blank=True, max_length=255, null=True)),
                ('urls', models.URLField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.schools')),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='FeeStructures',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('categories', models.JSONField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
            options={
                'db_table': 'fee_structures',
            },
        ),
        migrations.CreateModel(
            name='StudentsParents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parents.parents')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
            options={
                'db_table': 'student_parents',
            },
        ),
        migrations.CreateModel(
            name='VirtualAccounts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('balance', models.FloatField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.students')),
            ],
            options={
                'db_table': 'virtual_accounts',
            },
        ),
    ]
