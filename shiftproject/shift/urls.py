from django.urls import path
from . import views

app_name='shift'

urlpatterns=[
    path('edit/',views.edit,name='edit'),
    path('authorize/',views.authorize,name='authorize'),
    path('confirm/',views.confirm,name='confirm'),
    path('addShift/',views.add_shift,name='add_shift'),
    path('listShift/',views.get_shift,name='get_shift'),
    path('confirmShift/',views.confirmShift,name='confirm_shift'),
    path('authorize/authorize_detail/', views.authorize_detail, name='authorize_detail'),
    path('authorizeShift/<int:id>', views.authorizeShift, name='authorizeShift'),
    path('delete/',views.delete,name='delete'),
    path('delete/delete_detail/', views.delete_detail, name='delete_detail'),
    path('deleteShift/<int:id>', views.deleteShift, name='deleteShift'),
]
