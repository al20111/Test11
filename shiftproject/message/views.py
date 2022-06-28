from django.shortcuts import redirect, render
from django.views.generic import ListView
from sympy import use
from .models import Message,Board,Opinion
from .forms import MessageForm
from django.contrib.auth.models import User
# from account import User

def GetDestinationList(user_id):
    dest_list = [10001,10002,10003]
    dest_name_list = ["Taro","Miko","Fuyu"]
    '''ログイン情報対応版作成中
    dest_list = User.objects()
    '''
    return dest_list,dest_name_list

def GetDestinationInfo(request,user_id):
    dest_list,dest_name_list = GetDestinationList(user_id)
    flag,unread_list = Message().CalcUnreadNumberList(user_id,dest_list)
    dest_zip = zip(dest_list,dest_name_list,unread_list)
    '''ログイン情報対応版作成中
    ind_ID = user_id
    user = User.objects.filter(id = user_id).values("id","name")
    dest = User.objects.values('id', 'name')
    if request.method == "POST":
        return render(
            request,
            "message/history.html",
            {'user':user,'dest':dest}
        )
    else:
        return render(
            request,
            "message/history.html",
        )
    '''
    if not flag:
        return render(
            request,
            'message/select_destination.html',
            {'dest_list':dest_zip}
        )
    return render(
        request,
        'message/select_destination.html',
        {'dest_list':dest_zip,'user_id':user_id}
    )

def send(request):# send(request,user,dest):
    ind_ID = 10000  #ind_ID = user
    return redirect("message:select",user_id=ind_ID)


def GetMessageHistory(request,user_id,dest_id):
    ind_ID = user_id  #ind_ID = user
    dest_ID = dest_id
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
            return redirect("message:history",user_id=user_id,dest_id=dest_id)
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
