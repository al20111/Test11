from django.urls import path
from .import views

app_name='shift'

urlpatterns=[
    #掲示板・意見箱
    path('OB',views.ListOBView.as_view(),name='OB'),
    path('OB/board_edit/<int:pk>/',views.UpdateViewBoradView.as_view(),name='board-edit'),
    path('OB/board_detail/<int:pk>/',views.DetailBoardView.as_view(),name='board-detail'),
    path('OB/opinion_create/',views.CreateOpinionView.as_view(),name='opinion-create'),
    path('OB/opinion_list/',views.ListOpinionView.as_view(),name='opinion-list'),
    #店舗選択
    path('staff_create',views.CreateStaffView.as_view(),name='store-info'),
    # メッセージ送信(送信先選択)
    path('send/',views.send,name='send'),
    path('select_destination/<slug:user_id>/', views.get_destination_info, name='select'),
    # メッセージ送信(メッセージ履歴)
    path('history/<slug:dest_id>/', views.get_message_history, name='history'),
    path('update_history/', views.ajax_update_history, name='update_history'),

    path('edit/',views.edit,name='edit'),
    path('confirm/',views.confirm,name='confirm'),
    path('confirm_author/',views.confirm_author,name='confirm_author'),
    path('addShift/',views.add_shift,name='add_shift'),
    path('listShift/',views.get_shift,name='get_shift'),
    path('confirmShift/',views.confirmShift,name='confirmShift'),
    path('confirmShiftAuthor/',views.confirmShiftAuthor,name='confirmShiftAuthor'),
    path('ShiftMine/',views.shiftMine,name='shiftMine'),
    path('ShiftOthers/',views.shiftOthers,name='shiftOthers'),
    path('authorize/',views.authorize,name='authorize'),
    path('authorize_detail/', views.authorize_detail, name='authorize_detail'),
    path('authorizeShift/<int:id>', views.authorizeShift, name='authorizeShift'),
    path('delete/',views.delete,name='delete'),
    path('delete_detail/', views.delete_detail, name='delete_detail'),
    path('deleteShift/<int:id>', views.deleteShift, name='deleteShift'),
]
