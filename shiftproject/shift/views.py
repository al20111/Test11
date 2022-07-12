from calendar import isleap
from django.shortcuts import redirect, render
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from shift.forms import StaffCreateForm, MessageForm
from .models import Message, Board, Opinion, Store, Staff, ShiftData
from django.views.generic import(
    View,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
import time #給料計算
import json
from .forms import CalendarForm, ShiftForm, ConfirmForm
from django.middleware.csrf import get_token
from django.template import loader
from django.urls import reverse
from django.template.loader import render_to_string # ajax_update_history

# Create your views here.

'''
モジュール名: get_destination_list
作成者: 國枝直希
日付: 2022.7.10
機能要約: 各個人IDに対応するメッセージの送信先のID, 名前のリストを返す
'''

def get_destination_list(user_id):
    # 自分の所属する店舗IDを取得
    shop_id = Staff.objects.filter(user=user_id).values('store')[0]['store']

    # 同じ店舗IDに所属するユーザーを取得
    dest_id_list = Staff.objects.filter(store=shop_id).values('user')

    # 送信先のid, 名前のリストを作成
    dest_list = []
    dest_name_list = []
    for dest_id in dest_id_list:
        dest = dest_id['user']
        dest_name = User.objects.filter(
            id=dest_id['user']
        ).values_list('username', flat=True)[0]
        dest_list.append(dest)
        dest_name_list.append(dest_name)
    
    # 送信先のリストから自分自身を除外
    dest_list.pop(dest_list.index(user_id.id))
    dest_name_list.pop(dest_name_list.index(user_id.username))
    return dest_list, dest_name_list

'''
モジュール名: get_destination_info
作成者: 國枝直希
日付: 2022.7.10
機能要約: 各個人IDに対応するメッセージの送信先選択画面をレンダリングする
'''

def get_destination_info(request, user_id):
    user_id = request.user

    # 送信先のリスト, 未読数を取得
    dest_list, dest_name_list = get_destination_list(user_id)
    flag, unread_list = Message().calc_unread_number_list(user_id.id, dest_list)

    # テンプレートに送信先の名前と未読数をまとめて渡す準備
    dest_zip = zip(dest_name_list, unread_list)
    if not flag:
        return render(
            request,
            'shift/select_destination.html',
            {'dest_list': dest_zip}
        )
    return render(
        request,
        'shift/select_destination.html',
        {'dest_list': dest_zip}
    )

'''
モジュール名: send
作成者: 國枝直希
日付: 2022.7.10
機能要約: 送信先選択画面へ遷移する
'''

def send(request):
    return redirect("shift:select", user_id=request.user)

'''
モジュール名: ajax_update_history
作成者: 國枝直希
日付: 2022.7.10
機能要約: メッセージが送信先から送られたどうかと未読数, 最新のメッセージ履歴をJson形式で返す
'''

def ajax_update_history(request):
    ind_ID = request.user.id

    # GET リクエストの取得
    dest_name = request.GET['dest_name']

    # Ajax側に返す情報を取得
    dest_ID = User.objects.filter(username=dest_name).values_list('id',flat=True)[0]
    detect_flag, unread_number = Message().update_message_history(ind_ID,dest_ID)
    flag,messages = Message().get_message_history(ind_ID,dest_ID)
    context = {'messages':messages,'user_id':request.user,'dest_name':dest_name}

    # 最新のメッセージ履歴をテンプレートを使ってレンダリング
    content = render_to_string("shift/content.html",context,request)
    if detect_flag:
        # 相手からの新規メッセージがあった場合
        data = {'flag':True,'unread_number':unread_number,'content':content}
    else:
        # 相手からの新規メッセージがなかった場合
        data = {'flag':False,'unread_number':unread_number,'content':content}
    return JsonResponse(data)

'''
モジュール名: get_message_history
作成者: 國枝直希
日付: 2022.7.10
機能要約: 各個人IDに対応する選択された送信先とのメッセージ履歴をレンダリングし, 
         メッセージを送信した場合は内容をメッセージ履歴DBに保存する
'''

def get_message_history(request, dest_id):
    ind_ID = request.user.id
    dest_ID = User.objects.filter(username=dest_id).values_list('id', flat=True)[0]
    dest_name = dest_id

    # メッセージ履歴を取得
    messages = Message()
    flag, messages = messages.get_message_history(ind_ID, dest_ID)

    # POST の場合: メッセージ送信
    if request.method == "POST":
        message_info = Message(
            indivisual_id=ind_ID,
            dest_id=dest_ID,
            read_status=0
        )
        # request.POST: message内容のみ
        # メッセージ履歴に保存できるようformにインスタンスを提供
        form = MessageForm(request.POST, instance=message_info)
        if form.is_valid():
            message = form.save(commit=False)
            message.post = messages
            message.save()
            return redirect("shift:history", dest_id=dest_id)
    else:
        # GET の場合は空のフォームを作成
        form = MessageForm()

    if not flag:
        return render(
            request,
            'shift/history.html',
            {'messages': messages, 'form': form,
            'user_id': request.user, 'dest_name': dest_name}
        )
    return render(
        request,
        'shift/history.html',
        {'messages': messages, 'form': form,
        'user_id': request.user, 'dest_name': dest_name}
    )

'''
モジュール名:  ListOBView
作成者:  叶恒志
日付:  2022.7.10
機能要約:  店舗ごとの掲示板送信・確認ページや意見送信・意見箱ページを表示
'''
class ListOBView(LoginRequiredMixin, ListView):
    model = Board
    template_name = 'shift/board_list.html'
# 今ログインいているユーザーが所属している店舗に関するページを表示
    def get_queryset(self):
        store = Staff.objects.get(user=self.request.user)
        store_id = store.store
        queryset = super().get_queryset()
        return queryset.filter(store=store_id)

'''
モジュール名:  UPdateViewBoradView
作成者:  叶恒志
日付:  2022.7.10
機能要約:  店舗ごとの掲示板内容を更新する
'''
class UpdateViewBoradView(LoginRequiredMixin, UpdateView):
    model = Board
    fields = (['text'])
    template_name = 'shift/board_edit.html'
    success_url = reverse_lazy('shift:OB')

'''
モジュール名:  DetailBoardView
作成者:  叶恒志
日付:  2022.7.10
機能要約:  店舗ごとの掲示板内容を表示する
'''
class DetailBoardView(LoginRequiredMixin, DetailView):
    model = Board
    fields = (['text'])
    template_name = 'shift/board_detail.html'

'''
モジュール名:  CreateOpinionView
作成者:  叶恒志
日付:  2022.7.10
機能要約:  店舗ごとの意見箱内容を更新する
'''

class CreateOpinionView(LoginRequiredMixin, CreateView):
    model = Opinion
    fields = (['text'])
    template_name = 'shift/opinion_create.html'
    success_url = reverse_lazy('shift:opinion-create')
    #現在ログインしているユーザーのIDをformに入れる 
    def form_valid(self, form):
        store = Staff.objects.get(user=self.request.user)
        store_id = store.store
        form.instance.store = store_id
        return super().form_valid(form)
'''
モジュール名:  ListOpinionView
作成者:  叶恒志
日付:  2022.7.10
機能要約:  店舗ごとの意見箱内容を表示する
'''
class ListOpinionView(LoginRequiredMixin, ListView):
    model = Opinion
    template_name = 'shift/opinion_list.html'
    success_url = reverse_lazy('shift:opinion-list')

    def get_queryset(self):
        store = Staff.objects.get(user=self.request.user)
        store_id = store.store
        queryset = super().get_queryset()
        return queryset.filter(store=store_id)

'''
モジュール名:  CreateStaffView
作成者:  叶恒志
日付:  2022.7.10
機能要約:  店舗とユーザーを紐づける
'''

class CreateStaffView(LoginRequiredMixin, CreateView):
    model = Staff
    form = StaffCreateForm
    fields = (['store'])
    template_name = 'shift/store_create.html'
    success_url = reverse_lazy('index')
    #すでに店舗を登録しているユーザーにはメニュー画面を表示させる
    def get_template_names(self):
        if Staff.objects.filter(user=self.request.user).exists():
            template_name='index.html'
        else:
            template_name='shift/store_create.html'

        return [template_name]

    #現在ログインしているユーザーのIDをformに入れる
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



'''
モジュール名: edit
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: カレンダーを表示する
'''
def edit(request):
    shift = ShiftData.objects.filter(user_id=request.user.id)
    get_token(request)
    #template = loader.get_template('shift/edit.html') #カレンダーを表示する
    #return HttpResponse(template.render())
    return render(request, 'shift/edit.html', {'shift_list':shift},)

'''
モジュール名: add_shift
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: データベースにシフトの登録を行う
'''
def add_shift(request):
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
    store = Staff.objects.get(user=request.user,)

    # 登録処理
    shift = ShiftData(
        user_id=request.user,
        date=formatted_date,
        start_time=start_time,
        end_time=end_time,
        confirmed_flag=0,
        store_id=store.store,
    )
    shift.save()

    # 空を返却
    return HttpResponse("edit")

'''
モジュール名: get_shift
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: カレンダーに表示するイベントをデータベースから取得する
'''
def get_shift(request):
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
        date__lt=formatted_end_date, date__gt=formatted_start_date, user_id=request.user,
    )

    # fullcalendarのため配列で返却
    list = []
    for shift in shifts:
        if(shift.start_time % 100 == 0):
            start_min = "00"
        else:
            start_min = str(shift.start_time % 100)
        if(shift.end_time % 100 == 0):
            end_min = "00"
        else:
            end_min = str(shift.end_time % 100)
        Time = str(shift.start_time//100) + ":" + start_min + \
            "-" + str(shift.end_time//100) + ":" + end_min
        list.append(
            {
                "title": Time,
                "start": shift.date,
                "end": shift.date,
            }
        )

    return JsonResponse(list, safe=False)

'''
モジュール名: confirm
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: 従業員の閲覧画面でカレンダーを表示させる
'''
def confirm(request):
    get_token(request)
    shift = ShiftData.objects.filter(user_id=request.user.id)
    return render(request, 'shift/confirm.html', {'shift_list':shift},)

'''
モジュール名: confirm_author
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: 雇用者の閲覧画面でカレンダーを表示させる
'''
def confirm_author(request):
    get_token(request)
    get_token(request)
    shift = ShiftData.objects.filter(user_id=request.user.id)
    return render(request, 'shift/confirm_author.html', {'shift_list':shift},)
'''
モジュール名: confirm_shift
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: 従業員の閲覧画面のカレンダーで表示させる承認済みのシフトをデータベースから取得する
'''
def confirm_shift(request):
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
        user_id=request.user, date__lt=formatted_end_date, date__gt=formatted_start_date, confirmed_flag=1,
    )
    list = []
    for shift in confirmShifts:
        if(shift.start_time % 100 == 0):
            start_min = "00"
        else:
            start_min = str(shift.start_time % 100)
        if(shift.end_time % 100 == 0):
            end_min = "00"
        else:
            end_min = str(shift.end_time % 100)
        Time = str(shift.start_time//100) + ":" + start_min + \
            "-" + str(shift.end_time//100) + ":" + end_min
        list.append(
            {

                "title": Time,
                "start": shift.date,
                "end": shift.date,
            }
        )
    return JsonResponse(list, safe=False)

'''
モジュール名: confirm_shift_author
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: 雇用者の閲覧画面のカレンダーで表示させるシフト（承認・未承認）をデータベースから取得する
'''
def confirm_shift_author(request):
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
    Store_id = Staff.objects.get(user=request.user,)
    confirmShifts = ShiftData.objects.filter(
        date__lt=formatted_end_date, date__gt=formatted_start_date, store_id=Store_id.store,
    )
    list = []
    for shift in confirmShifts:
        list.append(
            {
                "title": shift.user_id,
                "start": shift.date,
                "end": shift.date,
            }
        )
    return JsonResponse(list, safe=False)

'''
モジュール名: shift_mine
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: 従業員の閲覧画面に表示させる該当月の給料計算を行う
'''
def shift_mine(request):
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
        user_id=request.user, date=formatted_date, confirmed_flag=1,
    )

    # 給料計算
    month = int(month)
    s = str(year) + " " + str(month) + " 01"

    if month == 2:
        if(isleap(int(year))):
            e = str(year) + " " + str(month) + " 29"
        else:
            e = str(year) + " " + str(month) + " 28"

    elif(month == 4 or month == 6 or month == 9 or month == 11):
        e = str(year) + " " + str(month) + " 30"
    else:
        e = str(year) + " " + str(month) + " 31"

    month_start = time.strptime(s, "%Y %m %d")
    month_end = time.strptime(e, "%Y %m %d")
    month_start = time.strftime(
        "%Y-%m-%d", month_start)
    month_end = time.strftime(
        "%Y-%m-%d", month_end)

    moneyShift = ShiftData.objects.filter(
        user_id=request.user, date__lte=month_end, date__gte=month_start, confirmed_flag=1,
    )
    store = Staff.objects.get(user=request.user,)
    permoney = Store.objects.get(name=store.store)

    money = 0

    for i in moneyShift:
        start_hour = i.start_time // 100
        start_min = i.start_time % 100
        end_hour = i.end_time // 100
        end_min = i.end_time % 100
        money += ((end_hour - start_hour) * 60 +
                  (end_min - start_min)) / 60 * permoney.wage

    list = []
    list.append(
        {
            "year": year, "month": month, "date": date, "confirmShift_S": confirmShift.start_time, "confirmShift_E": confirmShift.end_time, "user": confirmShift.user_id, "money": money,
        }
    )
    return JsonResponse(list, safe=False)

'''
モジュール名: shift_others
作成者: 若田佳菜子
日付: 2022.7.11
機能要約: 雇用者のカレンダーに表示させる従業員全員分のシフト（承認・未承認）をデータベースから取得する
'''
def shift_others(request):
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
    Store_id = Staff.objects.get(user=request.user,)
    Shifts = ShiftData.objects.filter(
        store_id=Store_id.store, date=formatted_date,
    )
    list = []
    for Shift in Shifts:
        list.append(
            {
                # str(year),str(month), str(date), str(Shift.start_time), str(Shift.end_time), str(Shift.user_id), str(Shift.confirmed_flag),
                "year": year, "month": month, "date": date, "start": Shift.start_time, "end": Shift.end_time, "user": Shift.user_id, "flag": Shift.confirmed_flag,
            }
        )

    return JsonResponse(list, safe=False)

# シフト承認

'''
モジュール名: authorize
作成者: 新井祐希
日付: 2022.7.12
機能要約: 日付入力画面を表示させる
'''
def authorize(request):
    """
    カレンダー画面
    """
    get_token(request)
    template = loader.get_template('shift/authorize.html')
    return HttpResponse(template.render({}, request))

'''
モジュール名: authorize_detail
作成者: 新井祐希
日付: 2022.7.12
機能要約: 未承認のシフトをデータベースから取得する
'''
def authorize_detail(request):
    template = loader.get_template('shift/authorize.html')
    d = request.POST['date_field']
    # shifts = ShiftData.objects.filter(date=d, confirmed_flag=0)
    store = Staff.objects.get(user=request.user)
    shifts = ShiftData.objects.filter(
        date=d, confirmed_flag=0, store_id=store.store)
    shift_list = []
    for shift in shifts:
        start_time = str(shift.start_time//100).zfill(2) + \
            ":" + str(shift.start_time % 100).zfill(2)
        end_time = str(shift.end_time//100).zfill(2) + ":" + \
            str(shift.end_time % 100).zfill(2)
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
        'authorize_text': "未承認のシフトはありません"
    }
    return HttpResponse(template.render(context, request))

'''
モジュール名: authorizeShift
作成者: 新井祐希
日付: 2022.7.12
機能要約: シフトを承認済にする
'''
def authorizeShift(request, id):
    shift = ShiftData.objects.get(id=id)
    shift.confirmed_flag = 1
    shift.save()
    return HttpResponseRedirect(reverse('shift:authorize'))

'''
モジュール名: delet
作成者: 新井祐希
日付: 2022.7.12
機能要約: 日付入力画面を表示させる
'''
def delete(request):
    template = loader.get_template('shift/delete.html')
    return HttpResponse(template.render({}, request))

'''
モジュール名: delete_detail
作成者: 新井祐希
日付: 2022.7.12
機能要約: シフトをデータベースから取得する
'''
def delete_detail(request):
    template = loader.get_template('shift/delete.html')
    d = request.POST['date_field']
    user = request.user
    shifts = ShiftData.objects.filter(user_id=user, date=d)
    shift_list = []
    for shift in shifts:
        start_time = str(shift.start_time//100).zfill(2) + \
            ":" + str(shift.start_time % 100).zfill(2)
        end_time = str(shift.end_time//100).zfill(2) + ":" + \
            str(shift.end_time % 100).zfill(2)
        if shift.confirmed_flag == 0:
            confirmed_flag = "未承認"
        else:
            confirmed_flag = "承認済"
        shift_list.append(
            {
                "id": shift.id,
                "date": shift.date,
                "start_time": start_time,
                "end_time": end_time,
                "confirmed_flag": confirmed_flag,
            }
        )
    context = {
        'shift_list': shift_list,
        'delete_text': "シフトはありません"
    }
    return HttpResponse(template.render(context, request))

'''
モジュール名: deleteShift
作成者: 新井祐希
日付: 2022.7.12
機能要約: シフトを削除する
'''
def deleteShift(request, id):
    shift = ShiftData.objects.get(id=id)
    shift.delete()
    return HttpResponseRedirect(reverse('shift:delete'))
