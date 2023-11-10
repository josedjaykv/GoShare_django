from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import VehiculoForm, TripForm, TripRatingForm, TripSearchForm
from .models import Vehiculo, Trip, TripRating
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.db.models import Count

# Create your views here.

def home(request):
    return render(request, 'home.html')

############################################# USUARIOS #############################################
    
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

    return render(request, 'signup.html', {'form': form, 'error': form.errors})

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
def profile(request):
    username = request.user.username

    return render(request, 'perfil.html', {
        'name': username
    }) 
    
############################################# VEHICULOS #############################################
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

############################################# VIAJES #############################################
@login_required
def trips(request):
    # Obtén todos los viajes excepto los del usuario actual
    trips = Trip.objects.filter(~Q(user=request.user))

    # Obtén los viajes del usuario actual
    mytrips = Trip.objects.filter(user=request.user)
    
    # Calcula la cantidad de asientos ocupados para cada viaje
    trips_with_occupied_seats = trips.annotate(
        occupied_seats=Count('passengers')
    )

    if request.method == 'POST':
        form = TripSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            
            # Realiza la búsqueda en los viajes
            trips = Trip.objects.filter(
                Q(user__username__icontains=search_query) |  # Búsqueda en el nombre de usuario
                Q(startingPlace__icontains=search_query) |  # Búsqueda en el lugar de inicio
                Q(arrivalPlace__icontains=search_query)  # Búsqueda en el lugar de llegada
            )
        else:
            # no muestra nada
            trips = Trip.objects.none()
            
    else:
        form = TripSearchForm()
        trips = Trip.objects.none()

    # Filtra los viajes por la condición trip.completed == False
    trips = trips.filter(completed=False)
    trips_with_occupied_seats = trips_with_occupied_seats.filter(completed=False)
    mytrips = mytrips.filter(completed=False)
    
    return render(request, 'trips.html', {
        'mytrips': mytrips,
        'trips': trips_with_occupied_seats,
        'search_form': form,
        'search_trips': trips,
    })




def my_trips(request):
    # Obtén los viajes creados por el usuario actual
    mytrips = Trip.objects.filter(user=request.user)
    
    # Obtén los viajes en los que el usuario ha estado como pasajero
    trips_as_passenger = Trip.objects.filter(passengers=request.user)

    return render(request, 'my_trips.html', {
        'mytrips': mytrips,
        'trips_as_passenger': trips_as_passenger,
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
                'form': form,
                'error': "Por favor provee datos validos"
            })
    else:
        # Si es una solicitud GET, simplemente crea una instancia del formulario.
        return render(request, 'create_trip.html', {
            'form': TripForm(user=request.user)
        })


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    passengers = trip.passengers.all()

    # Comprueba si el usuario actual es el creador del viaje
    is_owner = request.user == trip.user

    # Comprueba si el usuario actual ya es pasajero en el viaje
    is_passenger = request.user in passengers

    # Obtén la calificación del conductor (rated_driver) para este viaje
    rated_driver = TripRating.objects.filter(user=request.user, trip=trip).first()

    if request.method == 'POST':
        if is_owner:
            # Si el usuario es el creador, permite la edición del viaje
            form = TripForm(user=request.user, data=request.POST, instance=trip)
            if form.is_valid():
                form.save()
                return redirect('trips')
        elif not is_passenger:
            # Si el usuario no es el creador ni un pasajero, permite unirse al viaje
            trip.passengers.add(request.user)
            return redirect('trips')
    else:
        # Si es una solicitud GET, muestra la información del viaje
        form = TripForm(user=request.user, instance=trip) if is_owner else None
        ratinform = TripRatingForm(request.POST)

    
    return render(request, 'trip_detail.html', {
        'trip': trip,
        'form': form,
        'ratinform': ratinform,
        'is_owner': is_owner,
        'is_passenger': is_passenger,
        'rated_driver': rated_driver, 
    })


def join_trip(request, trip_id):
    # Obtiene el viaje al que el usuario desea unirse
    trip = get_object_or_404(Trip, pk=trip_id)

    # Verifica si hay asientos disponibles
    if trip.numseatsfree <= 0:
        return HttpResponseBadRequest("No hay asientos disponibles en este viaje.")

    # Agrega al usuario actual a la lista de pasajeros y disminuye numseatsfree
    trip.passengers.add(request.user)
    trip.numseatsfree -= 1
    trip.save()

    return redirect('trips')

@login_required
def leave_trip(request, trip_id):
    # Obtén el viaje
    trip = get_object_or_404(Trip, pk=trip_id)

    # Verifica si el usuario actual es un pasajero del viaje
    if request.user in trip.passengers.all():
        # Elimina al usuario de la lista de pasajeros
        trip.passengers.remove(request.user)
        
        # Actualiza numseatsfree
        trip.numseatsfree += 1
        trip.save()

    return redirect('trip_detail', trip_id=trip_id)

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk = trip_id, user = request.user)
    if request.method == 'POST':
        trip.delete()
        return redirect('trips')
    
@login_required
def finalize_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.user == trip.user and trip.numseatsfree == 0:
        # El usuario es el creador del viaje y todos los asientos están ocupados
        trip.completed = True
        trip.save()

    return redirect('trip_detail', trip_id=trip.id)

@login_required
def rate_driver(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    # Verificar si el usuario ya calificó al conductor para este viaje
    existing_rating = TripRating.objects.filter(user=request.user, trip=trip).first()

    if existing_rating:
        return redirect('trip_detail', trip_id=trip.id)

    if request.method == 'POST':
        form = TripRatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']

            # Crear una instancia de TripRating y guardarla en la base de datos
            rating = TripRating()
            rating.user = request.user
            rating.trip = trip
            rating.driver = trip.user
            rating.rating = rating_value
            rating.save()

            return redirect('trip_detail', trip_id=trip.id)
    else:
        form = TripRatingForm()

    return render(request, 'trip_detail.html', {
        'trip': trip,
        'form': form,
    })


