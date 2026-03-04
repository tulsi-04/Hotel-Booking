from django.db import models
from django.conf import settings
from hotels.models import Room

class AvailabilityCalendar(models.Model):
    room = models.ForeignKey(Room, related_name='availabilities', on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)
    dynamic_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('room', 'date')

    def __str__(self):
        return f"{self.room} on {self.date} - {'Available' if self.is_available else 'Booked'}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELED', 'Canceled'),
    )
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE, limit_choices_to={'role': 'CUSTOMER'})
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.customer.username}"
