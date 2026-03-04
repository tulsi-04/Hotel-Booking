from django.contrib import admin
from .models import Amenity, Hotel, RoomType, Room, HotelImage, Review

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'location', 'rating', 'is_approved')
    list_filter = ('is_approved', 'rating', 'location')
    search_fields = ('name', 'location')
    inlines = [HotelImageInline, RoomTypeInline]
    actions = ['approve_hotels']

    def approve_hotels(self, request, queryset):
        queryset.update(is_approved=True)
    approve_hotels.short_description = "Approve selected hotels"

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name', 'capacity', 'base_price')
    inlines = [RoomInline]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'is_available')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'customer', 'rating', 'created_at')
