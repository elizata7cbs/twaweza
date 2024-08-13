from django.db import models
from students.models.StudentsModel import Students


class VirtualAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'wallets'


