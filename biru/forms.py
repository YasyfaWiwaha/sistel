from django import forms
from django.utils.translation import gettext as _

class FacilityForm(forms.Form):
    facility_name = forms.CharField(label="facility_name",required=True)