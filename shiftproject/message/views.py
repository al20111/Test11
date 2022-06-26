from typing import List
from django.shortcuts import redirect, render
from django.views.generic import ListView
from sympy import use
from .models import Message,Board,Opinion
from .forms import MessageForm
from django.contrib.auth.models import User
# from account import User

def GetDestinationList(user_id,shop_ID):
    dest_list = [10001,10002,10003]
    dest_name_list = ["Taro","Miko","Fuyu"]
    '''ログイン情報対応版作成中
    dest_list = 
    '''
    return dest_list,dest_name_list

def GetDestinationInfo(request,user_id,shop_ID):
    ind_ID = 10000
    shop_ID = 0
    dest_list,dest_name_list = GetDestinationList(shop_ID)
    unread_list = Message().CalcUnreadNumberList(dest_list)
    '''ログイン情報対応版作成中
    ind_ID = user_id
    user = User.objects.filter(id = user_id).values("id","name")
    dest = User.objects.values('id', 'name')
    if request.method == "POST":
        return render(
            request,
            "message/send.html",
            {'user':user,'dest':dest}
        )
    else:
        return render(
            request,
            "message/send.html",
        )
    '''
    return render(
        request,
        'message/select_destination.html',
        {'dest_list':dest_list,'dest_name_list':dest_name_list,'unread_list': unread_list}
    )

def send(request):# send(request,user,dest):
    ind_ID = 10000  #ind_ID = user
    dest_ID = 10001
    messages = Message()
    flag,messages = messages.GetMessageHistory(ind_ID,dest_ID)
    
    if request.method == "POST":
        message_info = Message(
            indivisual_ID = ind_ID,
            dest_ID = dest_ID,
            read_status = 0
        )
        form = MessageForm(request.POST,instance=message_info)
        if form.is_valid():
            message = form.save(commit=False)
            message.post = messages
            message.save()
            return redirect("message:send")
    else:
        form = MessageForm()
    if not flag:
        return render(
            request,
            "message/send.html",
            {'somedata':100},
            {'form': form},
        )
    return render(
        request,
        'message/send.html',
        {'messages':messages,'form': form}
    )

def opinion(request):
    return render(
        request,
        'message/opinion.html',
        {'somedata':100},
    )
