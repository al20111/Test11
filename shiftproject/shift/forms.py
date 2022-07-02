from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class CalendarForm(forms.Form):

    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)

class ShiftForm(forms.Form):

    date = forms.IntegerField(required=True)
    time = forms.CharField(required=True, max_length=10)

class ConfirmForm(forms.Form):
    date = forms.IntegerField(required=True)

class DateForm(forms.Form):
    date_field = forms.DateField(widget=AdminDateWidget())
