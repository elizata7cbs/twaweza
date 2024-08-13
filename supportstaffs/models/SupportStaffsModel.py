from django.db import models
from schools.models import Schools
from supportstaffs.models import SupportCategory


class SupportStaff(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    idno = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.CharField(max_length=100)
    type = models.ForeignKey(SupportCategory, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'support_staffs'


class supportAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    bankName = models.CharField(max_length=100, null=True, blank=True)
    accountNumber = models.CharField(max_length=100, null=True, blank=True, unique=True)
    accountName = models.CharField(max_length=255, null=True, blank=True)
    staff = models.ForeignKey("supportstaffs.SupportStaff", on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'support_staffs_accounts'
