from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

def send(request):
    return render(
        request,
        'message/send.html',
        {'somedata':100},
    )

def opinion(request):
    return render(
        request,
        'message/opinion.html',
        {'somedata':100},
    )

