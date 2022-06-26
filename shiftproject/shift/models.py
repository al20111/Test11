from django.db import models
from platformdirs import user_config_dir


class Event(models.Model):
    start_date=models.DateField()
    end_date=models.DateField()
    event_name=models.CharField(max_length=100)

class ShiftData(models.Model):
    user_id=models.IntegerField()
    date=models.DateField()
    start_time=models.IntegerField()
    end_time=models.IntegerField()
    confirmed_flag=models.IntegerField()

