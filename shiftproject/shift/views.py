from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy
from shift.forms import StaffCreateForm
from .models import Board,Opinion,Store,Staff
from django.views.generic import(
    View,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)
# Create your views here.

class ListOBView(ListView):
    model=Board
    template_name='shift/board_list.html'
    def get_queryset(self):
        store=Staff.objects.get(user=self.request.user)
        store_id=store.store
        queryset=super().get_queryset()
        return queryset.filter(store=store_id)

class UpdateViewBoradView(UpdateView):
    model=Board
    fields=(['text'])
    template_name='shift/board_edit.html'
    success_url=reverse_lazy('shift:OB')

class DetailBoardView(DetailView):
    model=Board
    fields=(['text'])
    template_name='shift/board_detail.html'

class CreateOpinionView(CreateView):
    model=Opinion
    fields=(['text'])
    template_name='shift/opinion_create.html'
    success_url=reverse_lazy('shift:opinion-create')
    def form_valid(self,form):
        store=Staff.objects.get(user=self.request.user)
        store_id=store.store
        form.instance.store=store_id
        return super().form_valid(form)

class ListOpinionView(ListView):
    model=Opinion
    template_name='shift/opinion_list.html'
    success_url=reverse_lazy('shift:opinion-list')
    def get_queryset(self):
        store=Staff.objects.get(user=self.request.user)
        store_id=store.store
        queryset=super().get_queryset()
        return queryset.filter(store=store_id)

class CreateStoreView(LoginRequiredMixin,CreateView):
    model=Staff
    form=StaffCreateForm
    fields=(['store'])
    template_name='shift/store_create.html'
    success_url=reverse_lazy('index')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)