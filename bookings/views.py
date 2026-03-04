from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import customer_required
from hotels.models import RoomType, Room
from .models import Booking, AvailabilityCalendar
from django.contrib import messages
from datetime import datetime, date

@login_required
@customer_required
def checkout_view(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid dates provided.")
            return redirect('hotel_detail', hotel_id=room_type.hotel.id)
            
        if check_in >= check_out:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('hotel_detail', hotel_id=room_type.hotel.id)
            
        if check_in < date.today():
            messages.error(request, "Cannot book in the past.")
            return redirect('hotel_detail', hotel_id=room_type.hotel.id)

        # Basic real-time availability check
        available_rooms = room_type.rooms.filter(is_available=True)
        booked_rooms = Booking.objects.filter(
            room__in=available_rooms,
            status__in=['PENDING', 'CONFIRMED'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
        
        free_rooms = available_rooms.exclude(id__in=booked_rooms)
        
        if not free_rooms.exists():
            messages.error(request, "No rooms of this type are available for the selected dates.")
            return redirect('hotel_detail', hotel_id=room_type.hotel.id)
            
        room_to_book = free_rooms.first()
        days = (check_out - check_in).days
        total_price = days * room_type.base_price # Simplified for now
        
        booking = Booking.objects.create(
            customer=request.user,
            room=room_to_book,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='PENDING'
        )
        
        # Payment integration gets called here eventually
        messages.success(request, "Booking successful! Pending payment.")
        return redirect('my_bookings')
        
    return render(request, 'bookings/checkout.html', {'room_type': room_type})

@login_required
@customer_required
def my_bookings(request):
    bookings = request.user.bookings.all().order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
@customer_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.check_in > date.today():
        booking.status = 'CANCELED'
        booking.save()
        messages.success(request, "Booking canceled successfully.")
    else:
        messages.error(request, "Cannot cancel booking on or after check-in date.")
    return redirect('my_bookings')
