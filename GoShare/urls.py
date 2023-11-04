from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Usuarios
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),

    # Vehículos
    path('vehicles/', views.vehiculos, name='vehiculos'),
    path('vehicles/create/', views.create_vehiculo, name='create_vehiculo'),
    path('vehicles/<int:vehiculo_id>/', views.vehiculo_detail, name='vehiculo_detail'),
    path('vehicles/<int:vehiculo_id>/delete/', views.delete_vehiculo, name='delete_vehiculo'),

    # Viajes
    path('trips/', views.trips, name='trips'),
    path('trips/mine/', views.my_trips, name='my_trips'),
    path('trips/create/', views.create_trip, name='create_trip'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('trips/<int:trip_id>/join/', views.join_trip, name='join_trip'),
    path('trips/<int:trip_id>/leave/', views.leave_trip, name='leave_trip'),    
    path('trip/finalize/<int:trip_id>/', views.finalize_trip, name='finalize_trip'),
    path('trip/rate/<int:trip_id>/', views.rate_driver, name='rate_driver'),
   
]
