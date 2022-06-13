from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm

def index_view(request):
    return render(request,'account/index.html',{'somedata':100})


class SignupView(CreateView):
    model=User
    form_class=SignupForm
    template_name='accounts/signup.html'
    success_url=reverse_lazy('index')

