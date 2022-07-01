from .models import Staff
from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]

class StaffCreateForm(forms.ModelForm):
    class Meta:
        model=Staff
        fields=('store',)
    

    

