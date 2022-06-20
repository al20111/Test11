from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Board,Opinion
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)

def send(request):
    return render(
        request,
        'message/send.html',
    )

class ListOBView(ListView):
    model=Board
    template_name='massage/board_list.html'

class UpdateViewBoradView(UpdateView):
    model=Board
    fields=(['text'])
    template_name='message/board_edit.html'
    success_url=reverse_lazy('message:OB')

class DetailBoardView(DetailView):
    model=Board
    fields=(['text'])
    template_name='message/board_detail.html'

class CreateOpinionView(CreateView):
    model=Opinion
    fields=(['text'])
    template_name='message/opinion_create.html'
    success_url=reverse_lazy('message:opinion-create')

class ListOpinionView(ListView):
    model=Opinion
    template_name='message/opinion_list.html'
    success_url=reverse_lazy('message:opinion-list')






