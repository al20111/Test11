from django.urls import path
from . import views

app_name='message'

urlpatterns=[
    path('send/',views.send,name='send'),
    path('opinion/',views.opinion,name='opinion'),
    path('select_destination/<int:user_id>/', views.GetDestinationInfo, name='select'),
    path('history/<int:user_id>/<int:dest_id>/', views.GetMessageHistory, name='history'),
]