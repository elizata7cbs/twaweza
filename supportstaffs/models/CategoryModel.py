from django.db import models

from schools.models import Schools


class SupportCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'support_categories'



