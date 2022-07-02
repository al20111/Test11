from .models import Staff
from django import forms
class StaffCreateForm(forms.ModelForm):
    class Meta:
        model=Staff
        fields=('store',)