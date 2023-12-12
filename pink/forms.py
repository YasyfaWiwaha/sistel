from django import forms
from django.utils.translation import gettext as _

class SearchForm(forms.Form):
    max_price = forms.IntegerField(min_value=0,required=True)
    min_price = forms.IntegerField(min_value=0,required=True)

class ReviewForm(forms.Form):
    review = forms.CharField(required=True)
    rating = forms.CharField(required=True)