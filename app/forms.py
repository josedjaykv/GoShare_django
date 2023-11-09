from django import forms
from .models import Vehiculo, Trip, TripRating

class VehiculoForm(forms.ModelForm):    
    class Meta:
        model = Vehiculo
        fields = ['brand', 'model', 'plate', 'color',]

        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Chevrolet'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Spark GT'}),
            'plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' EJ: ABC-123'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'brand': 'Marca',
            'model': 'Modelo',
            'plate': 'Placa',
            'color': 'Color',
        }

class TripForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['vehiculo_disponible'].queryset = Vehiculo.objects.filter(user=user)

    vehiculo_disponible = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Elija un vehículo")

    class Meta:
        model = Trip
        fields = ['startingPlace', 'arrivalPlace', 'details', 'departureTime', 'travelDate', 'numseatsfree', 'vehiculo_disponible']

        widgets = {
            'startingPlace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Estación exposiciones'}),
            'arrivalPlace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Universidad EIA'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej: Manejo muy rápido, me dicen el rayo, o también Verstappen'}),
            'departureTime': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12:00', 'type' : 'time'}),
            'travelDate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2021-10-10', 'type' : 'date'}),
            'numseatsfree': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'}),
            'vehiculo_disponible': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'startingPlace': 'Lugar de Partida',
            'arrivalPlace': 'Lugar de Llegada',
            'details': 'Detalles',
            'departureTime': 'Hora de Salida',
            'travelDate': 'Fecha de Viaje',
            'numseatsfree': 'Número de Asientos Libres',
            'vehiculo_disponible': 'Vehículo Disponible',
        }

class TripRatingForm(forms.ModelForm):
    class Meta:
        model = TripRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': '1', 'min': '0', 'max': '5'}),
        }

class TripSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100, 
        required=False, 
        label='Buscador:',
        widget=forms.TextInput(attrs={'class': 'color-quaternary rounded input-buscador', 'placeholder': 'Buscar...'})
        )
