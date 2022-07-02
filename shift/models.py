from django.db import models
from django.conf import settings


class ShiftData(models.Model):
    user_id=models.CharField(max_length=100)
    date=models.DateField()
    start_time=models.IntegerField()
    end_time=models.IntegerField()
    confirmed_flag=models.IntegerField()
    store_id=models.CharField(max_length=20)


