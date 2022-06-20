from django.urls import path
from .import views

app_name='message'

urlpatterns=[
    path('OB',views.ListOBView.as_view(),name='OB'),
    path('send/',views.send,name='send'),
    path('OB/board_edit/<int:pk>/',views.UpdateViewBoradView.as_view(),name='board-edit'),
    path('OB/board_detail/<int:pk>/',views.DetailBoardView.as_view(),name='board-detail'),
    path('OB/opinion_create/',views.CreateOpinionView.as_view(),name='opinion-create'),
    path('OB/opinion_list/',views.ListOpinionView.as_view(),name='opinion-list'),

]
