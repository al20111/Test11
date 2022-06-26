from django.db import models
from django.db.models import Q
from sympy import true

# Create your models here.
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
        # Message.objects.
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
    shop_ID = models.PositiveIntegerField()
    board_message = models.CharField(max_length=5000)
    update_time = models.DateTimeField(auto_now=true)

    def GetBoardInfo(self,shop_ID):
        success_flag = 1
        board_info = Board.objects.filter(shop_ID=shop_ID)
        return success_flag,board_info
    
    def UpdateBoard(self,shop_ID,text):
        success_flag = 1
        new_board_info = Board(
            shop_ID = shop_ID,
            board_message = text
        )
        new_board_info.save(force_update=true)
        return success_flag

class Opinion(models.Model):
    shop_ID = models.PositiveIntegerField()
    opinion_message = models.CharField(max_length=2000)
    send_time = models.DateTimeField(auto_now_add=true)

    def GetOpinionBoxInfo(self,shop_ID):
        success_flag = 1
        opinionbox_info = Opinion.objects.filter(shop_ID=shop_ID)
        return success_flag,opinionbox_info
    
    def UpdateOpinionBox(self,shop_ID,text):
        success_flag = 1
        new_opinion_info = Opinion(
            shop_ID = shop_ID,
            opinion_message = text,
        )
        new_opinion_info.save(force_insert=true)
        return success_flag
