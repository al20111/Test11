from django.db import models

# Create your models here.
class Board(models.Model):
    text=models.TextField()

class Opinion(models.Model):
    text=models.TextField()


