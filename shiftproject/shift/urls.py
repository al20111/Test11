from django.urls import path
from . import views

app_name='shift'

urlpatterns=[
    path('edit/',views.index,name='edit'),
    path('authorize/',views.authorize,name='authorize'),
    path('confirm/',views.confirm,name='confirm'),
]
