from django import forms

class CreateRoomForm(forms.Form):
    
    nomor_kamar = forms.CharField(
        label='Nomor Kamar',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nomor Kamar',
            'type': 'text',
        }))

    harga = forms.DecimalField(
        label='Harga',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Harga',
        }))
    
    lantai = forms.DecimalField(
        label='Lantai',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Lantai',
        }))


class UpdateRoomForm(forms.Form):

    harga = forms.DecimalField(
        label='Harga',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Harga',
        }))
    
    lantai = forms.DecimalField(
        label='Lantai',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Lantai',
        }))