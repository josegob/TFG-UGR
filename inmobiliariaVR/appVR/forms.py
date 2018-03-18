from django import forms


class CasaForm(forms.Form):
    nombre_casa = forms.CharField(max_length=100, required=True)
    numero_habitaciones = forms.CharField(max_length=100, required=True)


