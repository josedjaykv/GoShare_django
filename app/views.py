from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import VehiculoForm, TripForm
from .models import Vehiculo, Trip
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('trips')
        else:
            # Verificar si las contraseñas no coinciden y agregar un mensaje de error
            if form.errors.get('password2') and "password_mismatch" in form.errors.get('password2'):
                messages.error(request, "Las contraseñas no coinciden.")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def vehiculos(request):
    # solo los vehiculos del usuario actual
    vehiculos = Vehiculo.objects.filter(user=request.user)
    #vehiculos = Vehiculo.objects.all()
    print(vehiculos)
    
    return render(request, 'vehiculo.html', {
        'vehiculos':vehiculos
    })

@login_required
def create_vehiculo(request):
    if request.method == 'GET':
        return render(request, 'create_vehiculo.html', {
            'form': VehiculoForm
        })
    else:
        try:
            form = VehiculoForm(request.POST)
            print(form)
            vehiculo = form.save(commit=False)
            vehiculo.user = request.user
            vehiculo.save()
            return redirect('vehiculos')
        except ValueError:
            print('Error al crear vehiculo')
            return render(request, 'create_vehiculo.html', {
                'form': VehiculoForm,
                'error': "Por favor provee datos validos"
            })

@login_required
def vehiculo_detail(request, vehiculo_id):
    if request.method == 'GET':
        # si la vehiculo existe la guarda si no muestra un error 404
        vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id, user = request.user)
        form = VehiculoForm(instance=vehiculo)
        return render(request, 'vehiculo_detail.html', {
            'vehiculo':vehiculo,
            'form':form
        })
    else:
        try:
            vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id, user = request.user)
            form = VehiculoForm(request.POST, instance=vehiculo)
            form.save()
            return redirect('vehiculos')
        except ValueError:
            return render(request, 'vehiculo_detail.html', {
            'vehiculo':vehiculo,
            'form':form,
            'error': 'Error al actualizar, campos por completar'
        })

@login_required
def delete_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id, user = request.user)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculos')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:  # me están enviando datos
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Nombre de usuario o contraseña incorrecto',
            })
        else:
            login(request, user)
            return redirect('trips')



    
        
@login_required
def trips(request):
    # Obtén todos los viajes excepto los del usuario actual
    trips = Trip.objects.filter(~Q(user=request.user))
    
    # Obtén los viajes del usuario actual
    mytrips = Trip.objects.filter(user=request.user)      
    
    return render(request, 'trips.html', {
        'mytrips':mytrips,
        'trips':trips
    })

@login_required
def my_trips(request):
    # solo los vehiculos del usuario actual que no están completadas
    mytrips = Trip.objects.filter(user=request.user)
    print(trips)
    
    return render(request, 'trips.html', {
        'mytrips':mytrips
    })

@login_required
def create_trip(request):
    if request.method == 'POST':
        # Si es una solicitud POST, pasa el usuario actual al formulario.
        form = TripForm(user=request.user, data=request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            vehiculo_seleccionado = form.cleaned_data['vehiculo_disponible']
            trip.vehiculo_disponible = vehiculo_seleccionado
            trip.user = request.user
            trip.save()
            return redirect('vehiculos')
        else:
            return render(request, 'create_trip.html', {
                'form': TripForm,
                'error': "Por favor provee datos validos"
            })
    else:
        # Si es una solicitud GET, simplemente crea una instancia del formulario.
        return render(request, 'create_trip.html', {
            'form': TripForm(user=request.user)
        })


@login_required
def trip_detail(request, trip_id):
    if request.method == 'GET':
        # si la tarea existe la guarda si no muestra un error 404
        trip = get_object_or_404(Trip, pk = trip_id, user = request.user)
        form = TripForm(instance=trip, user=request.user)
        return render(request, 'trip_detail.html', {
            'trip':trip,
            'form':form
        })
    else:
        try:
            trip = get_object_or_404(Trip, pk = trip_id, user = request.user)
            form = TripForm(request.POST, instance=trip)
            form.save()
            return redirect('trips')
        except ValueError:
            return render(request, 'trip_detail.html', {
            'trip':trip,
            'form':form,
            'error': 'Error al actualizar, campos por completar'
        })

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk = trip_id, user = request.user)
    if request.method == 'POST':
        trip.delete()
        return redirect('trips')


def profile(request):
    return render(request, 'perfil.html')   
