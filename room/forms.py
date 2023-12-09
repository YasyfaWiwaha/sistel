from django import forms

class createRoomForm(forms.Form):
    
    nomor_kamar = forms.CharField(
        label='Nomor Kamar',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nomor Kamar',
            'type': 'text',
            'readonly': 'true'
        }))

    harga = forms.DecimalField(
        label='Harga',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Harga',
            'readonly': 'true'
        }))
    
    lantai = forms.DecimalField(
        label='Harga',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Lantai',
            'readonly': 'true'
        }))


class updateRoomForm(forms.Form):

    nomor_kamar = forms.CharField(
        label='Nomor Kamar',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nomor Kamar',
            'type': 'text',
            'readonly': 'true'
        }))

    harga = forms.DecimalField(
        label='Harga',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Harga',
            'readonly': 'true'
        }))
    
    lantai = forms.DecimalField(
        label='Harga',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Lantai',
            'readonly': 'true'
        }))