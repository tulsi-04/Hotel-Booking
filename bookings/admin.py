from django.contrib import admin
from .models import AvailabilityCalendar, Booking

@admin.register(AvailabilityCalendar)
class AvailabilityCalendarAdmin(admin.ModelAdmin):
    list_display = ('room', 'date', 'is_available', 'dynamic_price')
    list_filter = ('is_available', 'date')
    search_fields = ('room__room_number', 'room__room_type__hotel__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'room', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'check_in')
    search_fields = ('customer__username', 'room__room_number', 'room__room_type__hotel__name')
