from django.db import models

from schools.models import Schools


class Suppliers(models.Model):
    PAYMENT_MODES = (
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Mpesa', 'Mpesa'),
    )
    id = models.AutoField(primary_key=True)
    supplierName = models.CharField(max_length=200)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    idno = models.CharField(max_length=200, unique=True)
    supplierEmail = models.CharField(max_length=200, null=True, blank=True, unique=True)
    supplierPhone = models.CharField(max_length=200, unique=True)
    supplierAddress = models.CharField(max_length=200)
    supplierWebsite = models.URLField()
    businessName = models.CharField(max_length=200)
    businessRegistrationNumber = models.CharField(max_length=200, null=True, blank=True, unique=True)
    kra = models.CharField(max_length=200, null=True, blank=True, unique=True)
    industry = models.CharField(max_length=200)
    productServices = models.CharField(max_length=200)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)
    bankName = models.CharField(max_length=200, null=True, blank=True, default='')
    accountName = models.CharField(max_length=200, null=True, blank=True, default='')
    accountNumber = models.CharField(max_length=200, null=True, blank=True, default='')
    mpesaName = models.CharField(max_length=200, null=True, blank=True, default='')
    mpesaNumber = models.CharField(max_length=100, null=True, blank=True, default='')
    openingBalance = models.FloatField(null=True, blank=True)
    paymentInterval = models.CharField(max_length=100)
    dateCreated = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'suppliers'


# class SuppliersAccount(models.Model):
#     supplier = models.OneToOneField(Suppliers, on_delete=models.CASCADE)
#     debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     date = models.DateField(auto_now_add=True)
#
#     @property
#     def balance(self):
#         # Calculate the balance
#         return self.debit - self.credit
#
#     def __str__(self):
#         # Return a string representation of the object
#         return f"Supplier: {self.supplier}, Balance: {self.balance}"
