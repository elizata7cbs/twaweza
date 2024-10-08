# Generated by Django 5.0.7 on 2024-07-22 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parents',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='parents',
            name='phone_number',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='parents',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
