import datetime

from django.contrib.auth.hashers import check_password
from django.db import models

from schools.models import Schools


class Parents(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    parent_idno = models.CharField(max_length=250)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=250, unique=True)
    first_login = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)

    parentType_choices = [
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Guardian', 'Guardian'),
        ('Sponsor', 'Sponsor'),
    ]
    parentType = models.CharField(max_length=10, choices=parentType_choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def _str_(self):
        return self.parentName

    class Meta:
        db_table = 'parents'
