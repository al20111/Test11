from .models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm
# Create your views here.
'''
モジュール名:  ListOpinionView
作成者:  村田哲彦
日付:  2022.7.10
機能要約:  新規会員を登録する
'''
class SignupView(CreateView):
    model=User
    form_class=SignupForm
    template_name='accounts/signup.html'
    success_url=reverse_lazy('accounts:login')



