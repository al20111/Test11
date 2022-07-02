from .models import Staff,Message
from django import forms
class StaffCreateForm(forms.ModelForm):
    class Meta:
        model=Staff
        fields=('store',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]
