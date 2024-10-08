# Generated by Django 5.0.7 on 2024-07-24 06:09

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'expense_types',
            },
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Expense Amount')),
                ('expenseID', models.CharField(default='TEMP', max_length=10, unique=True, verbose_name='Unique Expense ID')),
                ('currency', models.CharField(default='KES', max_length=10, verbose_name='Currency')),
                ('datePosted', models.DateField(auto_now_add=True, verbose_name='Date Posted')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('is_deleted', models.BooleanField(default=False)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15)),
                ('remaining_balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, verbose_name='Remaining Balance')),
                ('expensetypes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='expenses.expensetypes', verbose_name='Expense Type')),
            ],
            options={
                'db_table': 'expenses',
            },
        ),
    ]
