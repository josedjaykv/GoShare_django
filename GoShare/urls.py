from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),

    # Vehículos
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos/create/', views.create_vehiculo, name='create_vehiculo'),
    path('vehiculos/<int:vehiculo_id>/', views.vehiculo_detail, name='vehiculo_detail'),
    path('vehiculos/<int:vehiculo_id>/delete/', views.delete_vehiculo, name='delete_vehiculo'),

    # Viajes
    path('trips/', views.trips, name='trips'),
    path('trips/mine/', views.my_trips, name='my_trips'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),


    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),
]
