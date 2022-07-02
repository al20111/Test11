from django import forms

class CalendarForm(forms.Form):

    start_date = forms.IntegerField(required=True)
    end_date = forms.IntegerField(required=True)

class ShiftForm(forms.Form):

    date = forms.IntegerField(required=True)
    time = forms.CharField(required=True, max_length=10)

class ConfirmForm(forms.Form):
    date = forms.IntegerField(required=True)