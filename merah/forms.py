from django import forms
from django.utils.translation import gettext as _

class ComplaintForm(forms.Form):
    hotel_name = forms.CharField(required=True)
    hotel_chapter = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}),required=True)