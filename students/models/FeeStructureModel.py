from django.db import models
from students.models.StudentsModel import Students


class FeeStructures(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    categories = models.JSONField()
    date_created = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'fee_structures'
