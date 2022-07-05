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
import time
import json
from .forms import CalendarForm, ShiftForm, ConfirmForm
from django.middleware.csrf import get_token
from django.template import loader
from django.urls import reverse

# Create your views here.


def GetDestinationList(user_id):
    shop_id = Staff.objects.filter(user=user_id).values('store')[0]['store']
    dest_id_list = Staff.objects.filter(store=shop_id).values('user')
    dest_list = []
    dest_name_list = []
    for dest_id in dest_id_list:
        dest = dest_id['user']
        dest_name = User.objects.filter(
            id=dest_id['user']).values_list('username', flat=True)[0]
        dest_list.append(dest)
        dest_name_list.append(dest_name)
    dest_list.pop(dest_list.index(user_id.id))
    dest_name_list.pop(dest_name_list.index(user_id.username))
    return dest_list, dest_name_list


def GetDestinationInfo(request, user_id):
    user_id = request.user
    dest_list, dest_name_list = GetDestinationList(user_id)
    flag, unread_list = Message().CalcUnreadNumberList(user_id.id, dest_list)
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


def send(request):
    return redirect("shift:select", user_id=request.user)


def GetMessageHistory(request, dest_id):
    ind_ID = request.user.id
    dest_ID = User.objects.filter(
        username=dest_id).values_list('id', flat=True)[0]
    dest_name = dest_id
    messages = Message()
    flag, messages = messages.GetMessageHistory(ind_ID, dest_ID)

    if request.method == "POST":
        message_info = Message(
            indivisual_ID=ind_ID,
            dest_ID=dest_ID,
            read_status=0
        )
        form = MessageForm(request.POST, instance=message_info)
        if form.is_valid():
            message = form.save(commit=False)
            message.post = messages
            message.save()
            return redirect("shift:history", dest_id=dest_id)
    else:
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


class ListOBView(LoginRequiredMixin, ListView):
    model = Board
    template_name = 'shift/board_list.html'

    def get_queryset(self):
        store = Staff.objects.get(user=self.request.user)
        store_id = store.store
        queryset = super().get_queryset()
        return queryset.filter(store=store_id)


class UpdateViewBoradView(LoginRequiredMixin, UpdateView):
    model = Board
    fields = (['text'])
    template_name = 'shift/board_edit.html'
    success_url = reverse_lazy('shift:OB')


class DetailBoardView(LoginRequiredMixin, DetailView):
    model = Board
    fields = (['text'])
    template_name = 'shift/board_detail.html'


class CreateOpinionView(LoginRequiredMixin, CreateView):
    model = Opinion
    fields = (['text'])
    template_name = 'shift/opinion_create.html'
    success_url = reverse_lazy('shift:opinion-create')

    def form_valid(self, form):
        store = Staff.objects.get(user=self.request.user)
        store_id = store.store
        form.instance.store = store_id
        return super().form_valid(form)


class ListOpinionView(LoginRequiredMixin, ListView):
    model = Opinion
    template_name = 'shift/opinion_list.html'
    success_url = reverse_lazy('shift:opinion-list')

    def get_queryset(self):
        store = Staff.objects.get(user=self.request.user)
        store_id = store.store
        queryset = super().get_queryset()
        return queryset.filter(store=store_id)


class CreateStoreView(LoginRequiredMixin, CreateView):
    model = Staff
    form = StaffCreateForm
    fields = (['store'])
    template_name = 'shift/store_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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


def confirm(request):
    get_token(request)
    template = loader.get_template('shift/confirm.html')
    return HttpResponse(template.render())


def confirm_author(request):
    get_token(request)
    template = loader.get_template('shift/confirm_author.html')
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


def confirmShiftAuthor(request):
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


def shiftOthers(request):
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


def authorize(request):
    """
    カレンダー画面
    """
    get_token(request)
    template = loader.get_template('shift/authorize.html')
    return HttpResponse(template.render({}, request))


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


def authorizeShift(request, id):
    shift = ShiftData.objects.get(id=id)
    shift.confirmed_flag = 1
    shift.save()
    return HttpResponseRedirect(reverse('shift:authorize'))


def delete(request):
    template = loader.get_template('shift/delete.html')
    return HttpResponse(template.render({}, request))


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


def deleteShift(request, id):
    shift = ShiftData.objects.get(id=id)
    shift.delete()
    return HttpResponseRedirect(reverse('shift:delete'))
