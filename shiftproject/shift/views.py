import json
from .models import ShiftData
from django.http import Http404
import time
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .forms import CalendarForm,ShiftForm,ConfirmForm,DateForm

#シフト編集
def edit(request):
    """
    カレンダー画面
    """
    get_token(request)
    template = loader.get_template('shift/edit.html')
    return HttpResponse(template.render())

def add_shift(request):
    """
    シフト登録
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    shiftForm = ShiftForm(datas)
    if shiftForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    Date = datas["date"]
 #   start_time = datas["start_time"]
 #   end_time = datas["end_time"]
    Time = datas["time"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_date = time.strftime(
        "%Y-%m-%d", time.localtime(Date / 1000))

    splitedTime = Time.split('-')
    start_time = int(splitedTime[0])
    end_time = int(splitedTime[1])

    # 登録処理
    shift = ShiftData(
        user_id = 000000,
        date = formatted_date,
        start_time = start_time,
        end_time = end_time,
        confirmed_flag=0,
    )
    shift.save()

    # 空を返却
    return HttpResponse("edit")

def get_shift(request):
    """
    イベントの取得
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # FullCalendarの表示範囲のみ表示
    shifts = ShiftData.objects.filter(
        date__lt=formatted_end_date, date__gt=formatted_start_date , user_id= 0,
    )

    # fullcalendarのため配列で返却
    list = []
    for shift in shifts:
        if(shift.start_time%100==0) : start_min = "00"
        else : start_min = str(shift.start_time%100)
        if(shift.end_time%100==0) : end_min = "00"
        else : end_min = str(shift.end_time % 100)
        Time = str(shift.start_time//100) + ":" + start_min +"-"+ str(shift.end_time//100) + ":" + end_min
        list.append(
            {

                "title": Time,
                "start": shift.date,
                "end": shift.date,
            }
        )

    return JsonResponse(list, safe=False)

#シフト承認
def authorize(request):
    """
    カレンダー画面
    """
    get_token(request)
    template = loader.get_template('shift/authorize.html')
    context = {
        'form': DateForm()
    }
    return HttpResponse(template.render(context, request))

   # return render(
    #    request,
     #   'shift/authorize.html',
      #  {'somedata':100},
   # )

def authorize_detail(request):
    template = loader.get_template('shift/authorize_detail.html')
    d = request.POST.get('date_field')
    shifts = ShiftData.objects.filter(date=d, confirmed_flag=0)
    shift_list = []
    for shift in shifts:
        start_time = str(shift.start_time//100).zfill(2) + ":" + str(shift.start_time%100).zfill(2)
        end_time = str(shift.end_time//100).zfill(2) + ":" + str(shift.end_time%100).zfill(2)
        shift_list.append(
            {
                "id": shift.id,
                "user_id": shift.user_id,
                "date": shift.date,
                "start_time": start_time,
                "end_time": end_time,
            }
        )
    context = {
        'shift_list': shift_list,
    }
    return HttpResponse(template.render(context, request))

def authorizeShift(request, id):
    shift = ShiftData.objects.get(id=id)
    shift.confirmed_flag=1
    shift.save()
    return HttpResponseRedirect(reverse('shift:authorize'))

#シフト閲覧
def confirm(request):
    """
    カレンダー画面
    """
    get_token(request)
    template = loader.get_template('shift/confirm.html')
    return HttpResponse(template.render())

    #return render(
    #    request,
    #    'shift/confirm.html',
    #    {'somedata':100}
    #)

def confirmShift(request):
    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    confirmForm = ConfirmForm(datas)
    if confirmForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    Date = datas["date"]

     # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_date = time.strftime(
        "%Y-%m-%d", time.localtime(Date / 1000))

    confirmShift = ShiftData.objects.filter(
        user_id = 00000, date = formatted_date,
    )

    return JsonResponse(confirmShift, safe=False)
