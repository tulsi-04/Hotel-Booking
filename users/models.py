from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HOTEL_MANAGER', 'Hotel Manager'),
        ('CUSTOMER', 'Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.role}"
