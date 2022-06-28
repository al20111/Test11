from django.db import models
from django.conf import settings
# Create your models here.
class Staff(models.Model):
    user=models.OneToOneField('account.User',verbose_name='スタッフ',on_delete=models.CASCADE)
    store=models.ForeignKey('Store',verbose_name='店舗',on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.store}:{self.user}'
class Store(models.Model):
    name=models.CharField('店舗',max_length=20)
    wage=models.IntegerField('時給')
    
    def __str__(self):
        return self.name

class Board(models.Model):
    store=models.OneToOneField('Store',verbose_name='店舗',on_delete=models.CASCADE)
    text=models.TextField()

class Opinion(models.Model):
    store=models.ForeignKey('Store',verbose_name='店舗',on_delete=models.CASCADE)
    text=models.TextField()

