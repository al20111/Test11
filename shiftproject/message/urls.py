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
    path('store_create',views.CreateStoreView.as_view(),name='store-info'),
    path('select_destination/<slug:user_id>/', views.GetDestinationInfo, name='select'),
    path('history/<slug:dest_id>/', views.GetMessageHistory, name='history'),
    path('send_message/<slug:dest_id>/', views.ajax_send_message, name='send_message'),
    path('update_history/<slug:dest_id>/', views.ajax_update_history, name='update_history'),

]
