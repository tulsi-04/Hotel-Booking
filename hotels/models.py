from django.db import models
from django.conf import settings

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome class e.g., 'fa-wifi'")

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Amenities"

class Hotel(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'HOTEL_MANAGER'})
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    amenities = models.ManyToManyField(Amenity)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotels/')

    def __str__(self):
        return f"{self.hotel.name} Image"

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # e.g., Deluxe, Suite
    capacity = models.IntegerField(default=2)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

class Room(models.Model):
    room_type = models.ForeignKey(RoomType, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type.hotel.name} - Room {self.room_number}"

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'CUSTOMER'})
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.hotel.name}"
