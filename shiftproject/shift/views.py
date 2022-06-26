import json
from .models import Event
from .forms import EventForm
from django.http import Http404
import time
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.middleware.csrf import get_token

def edit(request):
    get_token(request)
    template=loader.get_template("shift/edit.html")
    return HttpResponse(template.render())

def add_event(request):
    """
    イベント登録
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]

    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))

    # 登録処理
    event = Event(
        event_name=str(event_name),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
    )
    event.save()

    # 空を返却
    return HttpResponse("edit")

def authorize(request):
    return render(
        request,
        'shift/authorize.html',
        {'somedata':100},
    )

def confirm(request):
    return render(
        request,
        'shift/confirm.html',
        {'somedata':100}
    )





