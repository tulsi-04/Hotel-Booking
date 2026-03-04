from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:booking_id>/', views.stripe_checkout, name='stripe_checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),
]
