from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

from .views import SignupView
from . import views

app_name='account'

urlpatterns=[
        path('',views.index_view,name='index'),
        path('login/',LoginView.as_view(),name='login'),
        path('logout/',LogoutView.as_view(),name='logout'),
        path('signup/',SignupView.as_view(),name='signup'),
]
