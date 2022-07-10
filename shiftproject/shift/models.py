from django.db import models
from django.db.models import Q
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
    indivisual_id = models.PositiveIntegerField()
    dest_id = models.PositiveIntegerField()
    message = models.CharField(max_length=2000)
    read_status = models.PositiveIntegerField()
    send_time = models.DateTimeField(auto_now_add=True)

    def CalcUnreadNumberList(self,indivisual_id,dest_id_list):
        success_flag = 1
        unread_number_list = []

        for dest_id in dest_id_list:
            unread_number = 0
            unread_number = Message.objects.filter(
                indivisual_id = dest_id,
                dest_id = indivisual_id,
                read_status = 0
            ).count()
            unread_number_list.append(unread_number)

        return success_flag,unread_number_list

    def GetMessageHistory(self,indivisual_id,dest_id):
        success_flag = 1
        # 相手から送られたメッセージに既読をつける
        dest_message = Message.objects.filter(
            Q(indivisual_id = dest_id, dest_id = indivisual_id)
        )
        for message in dest_message:
            message.read_status = 1
            message.save(force_update=True)
        
        message_history = Message.objects.filter(
            Q(indivisual_id = indivisual_id,dest_id = dest_id) 
            | Q(indivisual_id = dest_id, dest_id = indivisual_id)
        )
        return success_flag,message_history
    
    def UpdateMessageHistory(self,indivisual_id,dest_id):
        detect_flag = False
        dest_unread_number = Message.objects.filter(
            indivisual_id = dest_id,
            dest_id = indivisual_id,
            read_status = 0
        ).count()
        my_unread_number = Message.objects.filter(
            indivisual_id = indivisual_id,
            dest_id = dest_id,
            read_status = 0
        ).count()
        if not dest_unread_number == 0:
            detect_flag = True
        return detect_flag,my_unread_number

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