# Generated by Django 5.0.7 on 2024-07-18 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_students_date_of_admission_alter_students_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualaccounts',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
