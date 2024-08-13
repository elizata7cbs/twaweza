from django.db import models
from parents.models import Parents
import requests
from students.models.StudentsModel import Students


class StudentsParents(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'student_parents'
