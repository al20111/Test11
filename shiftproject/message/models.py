from django.db import models

# Create your models here.
class Board(models.Model):
    text=models.CharField(max_length=1000)

class Opinion(models.Model):
    text=models.CharField(max_length=1000)


