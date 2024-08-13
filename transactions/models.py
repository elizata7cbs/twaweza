from django.db import models


# Create your models here.
class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    ref_number = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=(
        ('CREDIT', 'CREDIT'),
        ('DEBIT', 'DEBIT'),
        ('OTHER', 'OTHER'),
    ))
    tran_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('SUCCESS', 'SUCCESS'),
        ('FAILED', 'FAILED'),
        ('PROCESSING', 'PROCESSING'),
        ('REJECTED', 'REJECTED'),
        ('CANCELLED', 'CANCELLED'),
        ('REFUNDED', 'REFUNDED'),
    ), default="SUCCESS")
    tran_ref = models.IntegerField(default=None, null=False, blank=False)  # connect to exact object
    tran_category = models.CharField(max_length=200)  # fee, supplies, expense,

    class Meta:
        db_table = 'transactions'


class Receipts(models.Model):
    id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    file_url = models.URLField(default=None)
    receipt_number = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'receipts'
