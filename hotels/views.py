from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required
from .models import Hotel, RoomType, Room, HotelImage
from django.contrib import messages

def hotel_list(request):
    hotels = Hotel.objects.filter(is_approved=True)
    # Add filtering logic later
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, is_approved=True)
    room_types = hotel.room_types.all()
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'room_types': room_types})

@login_required
@manager_required
def manager_dashboard(request):
    hotels = Hotel.objects.filter(manager=request.user)
    return render(request, 'hotels/manager_dashboard.html', {'hotels': hotels})

@login_required
@manager_required
def add_hotel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        
        hotel = Hotel.objects.create(
            manager=request.user,
            name=name,
            description=description,
            location=location,
            is_approved=False # Requires admin approval
        )
        messages.success(request, 'Hotel added successfully. Awaiting admin approval.')
        return redirect('manager_dashboard')
        
    return render(request, 'hotels/add_hotel.html')
