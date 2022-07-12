from .models import Staff, Message
from django import forms


class StaffCreateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('store',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]


class CalendarForm(forms.Form):

    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)


class ShiftForm(forms.Form):

    date = forms.IntegerField(required=True)
    time = forms.CharField(required=True, max_length=10)


class ConfirmForm(forms.Form):
    date = forms.IntegerField(required=True)
