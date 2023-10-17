from django import forms
from .models import Vehiculo, Trip

class VehiculoForm(forms.ModelForm):
    
    class Meta:
        model = Vehiculo
        fields = ['brand', 'model', 'color', 'numseats']

        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a brand'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a model'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'numseats': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'}),
        }

class TripForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['vehiculo_disponible'].queryset = Vehiculo.objects.filter(user=user)

    vehiculo_disponible = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Elija un vehículo")

    class Meta:
        model = Trip
        fields = ['startingPlace', 'arrivalPlace', 'details', 'departureTime', 'travelDate', 'numseatsfree', 'vehiculo_disponible', 'completed']

        widgets = {
            'startingPlace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Estación exposiciones'}),
            'arrivalPlace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Universidad EIA'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej: Manejo muy rápido, me dicen el rayo, o también Verstappen'}),
            'departureTime': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12:00'}),
            'travelDate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2021-10-10'}),
            'numseatsfree': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'}),
            'vehiculo_disponible': forms.Select(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }