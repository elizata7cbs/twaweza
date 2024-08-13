from django.db import models

from schools.models import Schools


class FeeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=True)


    class Meta:
        db_table = 'fee_category'

