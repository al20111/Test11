from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
    """
    カレンダー画面
    """
    template = loader.get_template('shift/edit.html')
    return HttpResponse(template.render())


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






