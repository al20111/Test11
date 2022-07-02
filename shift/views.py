import json
from .models import ShiftData
from django.http import Http404
import time
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .forms import CalendarForm,ShiftForm,ConfirmForm
from message.models import Staff,Store

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
    Time = datas["time"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_date = time.strftime(
        "%Y-%m-%d", time.localtime(Date / 1000))

    splitedTime = Time.split('-')
    start_time = int(splitedTime[0])
    end_time = int(splitedTime[1])

    store = Staff.objects.get(  user = request.user,)



    # 登録処理
    shift = ShiftData(
        user_id = request.user,
        date = formatted_date,
        start_time = start_time,
        end_time = end_time,
        confirmed_flag=0,
        store_id = store.store,
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
        date__lt=formatted_end_date, date__gt=formatted_start_date , user_id= request.user, 
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
    return HttpResponse(template.render())
    
   # return render(
    #    request,
     #   'shift/authorize.html',
      #  {'somedata':100},
   # )


#シフト閲覧
def confirm(request):
    """
    カレンダー画面
    """
    get_token(request)
    template = loader.get_template('shift/confirm.html')
    return HttpResponse(template.render())

def confirmShift(request):
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
    
    confirmShifts = ShiftData.objects.filter(
        user_id = request.user, date__lt=formatted_end_date, date__gt=formatted_start_date , confirmed_flag=1, 
    )
    list = []
    for shift in confirmShifts:
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

def shiftMine(request):
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
    DATE = datas["date"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_date = time.strftime(
        "%Y-%m-%d", time.localtime(DATE / 1000))
    year = time.strftime("%Y", time.localtime(DATE / 1000))
    month = time.strftime("%m", time.localtime(DATE / 1000))
    date = time.strftime("%d", time.localtime(DATE / 1000))

    confirmShift = ShiftData.objects.get(
        user_id = request.user, date = formatted_date, confirmed_flag=1,     
    )

    # 給料計算
    s = str(year) + " " + str(month) + " 01"
    if (month == 2 ):    e = str(year) + " " + str(month) + " 29" 
    elif( month == 4, month == 6, month ==9, month ==11) :  e = str(year) + " " + str(month) + " 30" 
    else :  e = str(year) + " " + str(month) + " 31" 
    month_start = time.strptime(s,"%Y %m %d")
    month_end = time.strptime(e, "%Y %m %d")
    month_start = time.strftime(
        "%Y-%m-%d", month_start)
    month_end = time.strftime(
        "%Y-%m-%d", month_end )
    moneyShift = ShiftData.objects.filter(
        user_id = request.user, date__lt=month_end, date__gt=month_start, confirmed_flag=1,
    )
    store = Staff.objects.get(user = request.user,  )
    permoney = Store.objects.get( name = store.store)
    
    money = 0

    for i in moneyShift :
        start_hour = i.start_time // 100
        start_min = i.start_time % 100
        end_hour = i.end_time // 100
        end_min = i.end_time % 100
        money += ((end_hour - start_hour ) * 60 + (end_min -start_min)) / 60 * permoney.wage
    
    list = []
    list.append(
        {
        "year" :year, "month":month, "date":date, "confirmShift_S" :confirmShift.start_time, "confirmShift_E" :confirmShift.end_time, "user" :confirmShift.user_id, "money" :money,
        }
    )

    return JsonResponse(list, safe=False)
