from django.db import models

# Create your models here.
from django.utils import timezone

class Service(models.Model):
    service_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.TextField(max_length = 250)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name
    



class ServiceBooking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')

    # Customer Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Booking Details
    booking_date = models.DateField()
    booking_time = models.TimeField()

    address = models.TextField()
    notes = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} - {self.service} - {self.booking_date}"
    


