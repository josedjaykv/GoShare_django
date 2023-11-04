from django.db import models
from django.contrib.auth.models import User

COLOR_CHOISES = [
        ('gris', 'Gris'),
        ('negro', 'Negro'),
        ('blanco', 'Blanco'),
        ('rojo', 'Rojo'),
        ('azul', 'Azul'),
        ('verde', 'Verde'),
        ('amarillo', 'Amarillo')        
    ]


# Create your models here.
class Vehiculo(models.Model):
    brand = models.CharField(max_length=100)   
    model = models.CharField(max_length=100)
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOISES,
        default='blanco'
    )  
    plate = models.CharField(max_length=10, default="")
    created = models.DateTimeField(auto_now_add = True)
    editionDate = models.DateTimeField(null = True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.model 
    
class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Asocia el viaje con un usuario
    startingPlace = models.CharField(max_length=100)
    arrivalPlace = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    departureTime = models.TimeField()
    travelDate = models.DateField()
    numseatsfree = models.IntegerField()
    passengers = models.ManyToManyField(User, related_name='trips_joined', blank=True)
    vehiculo_disponible = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, blank=True, null=True, default='Sin vehículo')
    created = models.DateTimeField(auto_now_add = True)
    editionDate = models.DateTimeField(null = True, blank=True)
    completed = models.BooleanField(default=False)
    datecompleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Viaje de {self.user.username} desde {self.startingPlace} hasta {self.arrivalPlace}'
    
class TripRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated_drivers')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'trip', 'driver')