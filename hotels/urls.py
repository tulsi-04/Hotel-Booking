from django.urls import path
from . import views

urlpatterns = [
    # Customer views
    path('', views.hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    
    # Manager views
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('add/', views.add_hotel, name='add_hotel'),
]
