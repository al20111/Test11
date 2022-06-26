from django.db import models

class Shifts(models.Model):
  _id = models.IntegerField()
  date = models.IntegerField()
  start = models.IntegerField()
  end = models.IntegerField()
  shiftcheck = models.BooleanField(default=False)

class Shifts(models.Model):
  _id = models.IntegerField()
  date = models.IntegerField()
  start = models.IntegerField()
  end = models.IntegerField()
