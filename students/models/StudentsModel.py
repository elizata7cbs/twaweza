from django.db import models
from schools.models import Schools


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    uniqueNumber = models.CharField(max_length=50, unique=True, blank=False)
    admNumber = models.CharField(max_length=255, unique=True, blank=False)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    parents = models.JSONField(null=True, blank=True, default=list)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=100)
    dob = models.CharField(max_length=150)
    date_of_admission = models.CharField(max_length=150)
    health_status = models.TextField()
    upi_number = models.CharField(max_length=255, blank=True, null=True)
    urls = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'students'


