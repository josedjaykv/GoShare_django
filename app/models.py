from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django.db import models



class CustomUser(AbstractUser):
    number_of_trips = models.IntegerField(default=0, blank=True)
    average_rating = models.FloatField(default=0.0, blank=True)

    # Agregar related_name para evitar conflictos en los accesores inversos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

class Vehiculo(models.Model):
    brand = models.CharField(max_length=25)   
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)    
    plate = models.CharField(max_length=10, default="")
    created = models.DateTimeField(auto_now_add = True)
    editionDate = models.DateTimeField(null = True, blank=True)
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.model 
    
class Trip(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Asocia el viaje con un usuario
    startingPlace = models.CharField(max_length=100)
    arrivalPlace = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    departureTime = models.TimeField()
    travelDate = models.DateField()
    numseatsfree = models.IntegerField()
    passengers = models.ManyToManyField(CustomUser, related_name='trips_joined', blank=True)
    vehiculo_disponible = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, blank=True, null=True, default='Sin vehículo')
    created = models.DateTimeField(auto_now_add = True)
    editionDate = models.DateTimeField(null = True, blank=True)
    completed = models.BooleanField(default=False)
    datecompleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Viaje de {self.CustomUser.username} desde {self.startingPlace} hasta {self.arrivalPlace}'
    
class TripRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rated_drivers')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'trip', 'driver')