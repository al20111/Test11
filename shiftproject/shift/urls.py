from django.urls import path
from . import views

app_name='shift'

urlpatterns=[
    path('edit/',views.edit,name='edit'),
    path('authorize/',views.authorize,name='authorize'),
    path('confirm/',views.confirm,name='confirm'),
    path('add/',views.add_event,name="add_event"),
    path("list/", views.get_events, name="get_events"),
]
