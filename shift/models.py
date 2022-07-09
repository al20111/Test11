from django.db import models
from django.db.models import Q
from sympy import true
from django.conf import settings
# Create your models here.
class Staff(models.Model):
    user=models.OneToOneField('accounts.User',verbose_name='スタッフ',on_delete=models.CASCADE)
    store=models.ForeignKey('Store',verbose_name='店舗',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store}:{self.user}'


class Store(models.Model):
    name=models.CharField('店舗',max_length=20)
    wage=models.IntegerField('時給')
    
    def __str__(self):
        return self.name

class Message(models.Model):
    indivisual_ID = models.PositiveIntegerField()
    dest_ID = models.PositiveIntegerField()
    message = models.CharField(max_length=2000)
    read_status = models.PositiveIntegerField()
    send_time = models.DateTimeField(auto_now_add=true)

    def CalcUnreadNumberList(self,indivisual_ID,dest_ID_list):
        success_flag = 1
        unread_number_list = []

        for dest_ID in dest_ID_list:
            unread_number = 0
            unread_number = Message.objects.filter(
                indivisual_ID = dest_ID,
                dest_ID = indivisual_ID,
                read_status = 0
            ).count()
            unread_number_list.append(unread_number)

        return success_flag,unread_number_list

    def GetMessageHistory(self,indivisual_ID,dest_ID):
        success_flag = 1
        # 相手から送られたメッセージに既読をつける
        dest_message = Message.objects.filter(
            Q(indivisual_ID = dest_ID, dest_ID = indivisual_ID)
        )
        for message in dest_message:
            message.read_status = 1
            message.save(force_update=true)
        
        message_history = Message.objects.filter(
            Q(indivisual_ID = indivisual_ID,dest_ID = dest_ID) 
            | Q(indivisual_ID = dest_ID, dest_ID = indivisual_ID)
        )
        return success_flag,message_history
    
    def UpdateMessageHistory(self,indivisual_ID,dest_ID,message):
        success_flag = 1
        new_message = Message(
            indivisual_ID = indivisual_ID,
            dest_ID = dest_ID,
            message = message,
            read_status = 0
        )
        new_message.save(force_insert=true)
        message_history = Message.objects.filter(
            Message(indivisual_ID = indivisual_ID) | Message(indivisual_ID = dest_ID)
        )
        return success_flag,message_history

class Board(models.Model):
    store=models.OneToOneField('Store',verbose_name='店舗',on_delete=models.CASCADE)
    text=models.TextField()


class Opinion(models.Model):
    store=models.ForeignKey('Store',verbose_name='店舗',on_delete=models.CASCADE)
    text=models.TextField()

class ShiftData(models.Model):
    user_id=models.CharField(max_length=100)
    date=models.DateField()
    start_time=models.IntegerField()
    end_time=models.IntegerField()
    confirmed_flag=models.IntegerField()
    store_id=models.CharField(max_length=20)