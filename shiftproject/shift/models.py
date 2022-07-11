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

    # 未読数のリストを返す
    def calc_unread_number_list(self,indivisual_id,dest_id_list):
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

    # 個人IDと送信先のIDに対応したメッセージ履歴を返す
    def get_message_history(self,indivisual_id,dest_id):
        success_flag = 1

        # 相手から送られたメッセージに既読をつける
        dest_message = Message.objects.filter(
            Q(indivisual_id = dest_id, dest_id = indivisual_id)
        )
        for message in dest_message:
            message.read_status = 1
            message.save(force_update=True)
        
        # メッセージ履歴を取得
        message_history = Message.objects.filter(
            Q(indivisual_id = indivisual_id,dest_id = dest_id) 
            | Q(indivisual_id = dest_id, dest_id = indivisual_id)
        )
        return success_flag,message_history
    
    # 新規メッセージが送られているかどうかと自分のメッセージの未読数を返す
    def update_message_history(self,indivisual_id,dest_id):
        detect_flag = False

        # 送信先の未読数を取得
        dest_unread_number = Message.objects.filter(
            indivisual_id = dest_id,
            dest_id = indivisual_id,
            read_status = 0
        ).count()

        # 自分の未読数を取得
        my_unread_number = Message.objects.filter(
            indivisual_id = indivisual_id,
            dest_id = dest_id,
            read_status = 0
        ).count()

        # 送信先の未読数が0でなければTrue
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