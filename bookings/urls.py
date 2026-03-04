from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:room_type_id>/', views.checkout_view, name='checkout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
