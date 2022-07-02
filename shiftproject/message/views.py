from django.shortcuts import redirect, render
from account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from message.forms import StaffCreateForm, MessageForm
from .models import Message,Board,Opinion,Store,Staff
from django.views.generic import(
    View,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)

def GetDestinationList(user_id):
    shop_id = Staff.objects.filter(user=user_id).values('store')[0]['store']
    dest_id_list = Staff.objects.filter(store=shop_id).values('user')
    dest_list = []
    dest_name_list = []
    for dest_id in dest_id_list:
        dest = dest_id['user']
        dest_name = User.objects.filter(id=dest_id['user']).values_list('username',flat=True)[0]
        dest_list.append(dest)
        dest_name_list.append(dest_name)
    dest_list.pop(dest_list.index(user_id.id))
    dest_name_list.pop(dest_name_list.index(user_id.username))
    return dest_list,dest_name_list

def GetDestinationInfo(request,user_id):
    user_id = request.user
    dest_list,dest_name_list = GetDestinationList(user_id)
    flag,unread_list = Message().CalcUnreadNumberList(user_id.id,dest_list)
    dest_zip = zip(dest_name_list,unread_list)
    if not flag:
        return render(
            request,
            'message/select_destination.html',
            {'dest_list':dest_zip}
        )
    return render(
        request,
        'message/select_destination.html',
        {'dest_list':dest_zip}
    )

def send(request):
    return redirect("message:select",user_id=request.user)


def GetMessageHistory(request,dest_id):
    ind_ID = request.user.id
    dest_ID = User.objects.filter(username=dest_id).values_list('id',flat=True)[0]
    dest_name = dest_id
    messages = Message()
    flag,messages = messages.GetMessageHistory(ind_ID,dest_ID)
    
    if request.method == "POST":
        message_info = Message(
            indivisual_ID = ind_ID,
            dest_ID = dest_ID,
            read_status = 0
        )
        form = MessageForm(request.POST,instance=message_info)
        if form.is_valid():
            message = form.save(commit=False)
            message.post = messages
            message.save()
            return redirect("message:history",dest_id=dest_id)
    else:
        form = MessageForm()
    if not flag:
        return render(
            request,
            'message/history.html',
            {'messages':messages,'form': form,'user_id':request.user,'dest_name':dest_name}
        )
    return render(
        request,
        'message/history.html',
        {'messages':messages,'form': form,'user_id':request.user,'dest_name':dest_name}
    )

class ListOBView(ListView):
    model=Board
    template_name='massage/board_list.html'
    def get_queryset(self):
        store=Staff.objects.get(user=self.request.user)
        store_id=store.store
        queryset=super().get_queryset()
        return queryset.filter(store=store_id)

class UpdateViewBoradView(UpdateView):
    model=Board
    fields=(['text'])
    template_name='message/board_edit.html'
    success_url=reverse_lazy('message:OB')

class DetailBoardView(DetailView):
    model=Board
    fields=(['text'])
    template_name='message/board_detail.html'

class CreateOpinionView(CreateView):
    model=Opinion
    fields=(['text'])
    template_name='message/opinion_create.html'
    success_url=reverse_lazy('message:opinion-create')
    def form_valid(self,form):
        store=Staff.objects.get(user=self.request.user)
        store_id=store.store
        form.instance.store=store_id
        return super().form_valid(form)
class ListOpinionView(ListView):
    model=Opinion
    template_name='message/opinion_list.html'
    success_url=reverse_lazy('message:opinion-list')
    def get_queryset(self):
        store=Staff.objects.get(user=self.request.user)
        store_id=store.store
        queryset=super().get_queryset()
        return queryset.filter(store=store_id)

class CreateStoreView(LoginRequiredMixin,CreateView):
    model=Staff
    form=StaffCreateForm
    fields=(['store'])
    template_name='message/store_create.html'
    success_url=reverse_lazy('account:index')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)





