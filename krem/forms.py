from django import forms
from django.utils.translation import gettext as _

class ReservationForm(forms.Form):
    check_in = forms.DateField(required=True,widget=forms.TextInput(attrs={'type':'date'}))
    check_out = forms.DateField(required=True,widget=forms.TextInput(attrs={'type':'date'}))