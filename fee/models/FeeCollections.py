from django.db import models

from parents.models import Parents
from schools.models import Schools
from students.models.StudentsModel import Students


class FeeCollections(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('virtual_account', 'Virtual Account'),
        ('Bank_cards', 'Bank Cards'),
        ('Bank_agent', 'Bank Agent'),
        ('M-pesa', 'M-pesa'),
        ('Cash', 'Cash'),
        ('counter', 'Over the Counter'),
    ]

    PAYMENT_TYPES = [
        ("DR", "DR"),
        ("CR", "CR"),
    ]

    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(Parents, on_delete=models.CASCADE)
    fee_category = models.ForeignKey("fee.FeeCategory", on_delete=models.CASCADE)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    payment_reference = models.CharField(max_length=50, unique=True)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES)
    receipt_number = models.CharField(max_length=100, unique=True, blank=False)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE_CHOICES)

    class Meta:
        db_table = 'fee_collections'


class FeeStudentBalances(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    balance = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)
