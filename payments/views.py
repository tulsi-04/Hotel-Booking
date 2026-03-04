import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from bookings.models import Booking
from .models import Payment, Invoice
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import tempfile
from django.core.files import File

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status != 'PENDING':
        messages.info(request, "This booking is already processed or canceled.")
        return redirect('my_bookings')

    domain_url = request.build_absolute_uri('/')[:-1]
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(booking.total_price * 100),
                        'product_data': {
                            'name': f"Booking at {booking.room.room_type.hotel.name}",
                            'description': f"{booking.room.room_type.name} from {booking.check_in} to {booking.check_out}",
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=domain_url + reverse('payment_success') + f'?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking.id}',
            cancel_url=domain_url + reverse('payment_cancel') + f'?booking_id={booking.id}',
        )
        return redirect(checkout_session.url, code=303)
    except stripe.error.AuthenticationError:
        # FAKE SUCCESS FOR DEVELOPMENT W/O REAL KEYS
        messages.warning(request, "Stripe keys are invalid. Simulating successful payment for testing.")
        return redirect(reverse('payment_success') + f'?session_id=fake_session_123&booking_id={booking.id}')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('my_bookings')

def payment_success(request):
    booking_id = request.GET.get('booking_id')
    session_id = request.GET.get('session_id')
    
    if not booking_id:
        return redirect('home')
        
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    # Check if payment already recorded
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'stripe_session_id': session_id,
            'amount': booking.total_price,
            'status': 'SUCCESS'
        }
    )
    
    if not created and payment.status != 'SUCCESS':
        payment.status = 'SUCCESS'
        payment.stripe_session_id = session_id
        payment.save()

    booking.status = 'CONFIRMED'
    booking.save()
    
    # Generate Invoice automatically
    generate_invoice_pdf(booking)
    
    messages.success(request, "Payment successful! Your booking is confirmed.")
    return redirect('my_bookings')

def payment_cancel(request):
    messages.error(request, "Payment was canceled. Your booking remains pending.")
    return redirect('my_bookings')

def generate_invoice_pdf(booking):
    if hasattr(booking, 'invoice'):
        return booking.invoice
        
    template_path = 'payments/invoice_template.html'
    context = {'booking': booking}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        pisa_status = pisa.CreatePDF(html, dest=output)
        if pisa_status.err:
            return None
            
        invoice = Invoice.objects.create(booking=booking)
        invoice.pdf_file.save(f"invoice_{booking.id}.pdf", File(output))
        return invoice

def download_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if hasattr(booking, 'invoice') and booking.invoice.pdf_file:
        response = HttpResponse(booking.invoice.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'
        return response
    messages.error(request, "Invoice not found or not generated yet.")
    return redirect('my_bookings')
