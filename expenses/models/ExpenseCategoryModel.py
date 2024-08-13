from django.db import models

from schools.models import Schools
from datetime import datetime


class ExpenseTypes(models.Model):
    name = models.CharField(max_length=100, unique=True)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'expense_types'
