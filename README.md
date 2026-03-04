# LuxeStay - Advanced Hotel Booking System

LuxeStay is a fully functional, production-ready Hotel Booking Application built with Django. It features role-based authentication, an Admin Panel, a Hotel Manager dashboard, a Customer booking flow, real-time availability, and Stripe payment integration. The design utilizes a modern gradient with luxury gold accents, glassmorphism, and smooth animations using Tailwind CSS and AOS.

## Features Included

### 1. Role-Based Authentication System
- **Roles:** Admin, Hotel Manager, Customer
- **Features:**
  - Email verification (prepared flag)
  - Role-based dashboard access
  - Session management

### 2. Admin Panel Features (via Django Admin)
- Add / Update / Delete hotels
- Manage room categories and amenities
- Manage ratings and pricing
- Control room availability
- Approve or reject hotel listings

### 3. Hotel Manager Features
- Manager Dashboard
- Add hotel details (name, location, description, rating)
- *Pending Admin Approval* workflow before listing is public

### 4. Customer Features
- Browse and search hotels
- Filter hotels by location and name
- View hotel details page, room available types, and amenities
- Check real-time room availability to prevent double scheduling
- Calculate total price automatically based on nights stayed
- Book room, online secure payment checkout (Stripe Test)
- Download booking invoice (PDF generated dynamically)
- View booking history list and cancel active bookings

### 5. Payment Integration
- Integration with Stripe Checkout (Test Mode)
- Secures transaction IDs and returns success callbacks
- Generates PDF invoices automatically (`xhtml2pdf`)

### 6. UI / UX Design
- **Theme:** Premium Luxury Hotel Theme
- **Color Palette:** Deep Navy (`#0A1F44`) and Gold (`#D4AF37`)
- **Effects:**
  - Modern gradients and glassmorphism cards.
  - Hover animations and smooth scroll revealing (AOS).
- Fully responsive on mobile and desktop.

### 7. Performance & Security Setup
- CSRF protection and role-based decorators to ensure secure access.
- Modular architecture with `core`, `users`, `hotels`, `bookings`, and `payments` apps.

## Prerequisites

- Python 3.9+ 
- Virtual environment wrapper (`venv`)

## Installation & Setup

1. **Clone the repository** (or download the source directory).
```bash
cd "Hotel Booking"
```

2. **Create a virtual environment and activate it:**
```bash
python -m venv venv
.\venv\Scripts\activate # Windows
# source venv/bin/activate # Mac/Linux
```

3. **Install the dependencies:**
```bash
pip install django pillow stripe django-crispy-forms crispy-tailwind xhtml2pdf
```

4. **Run Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a Superuser (Admin account):**
```bash
python manage.py createsuperuser
# Follow the prompts to set your username, email, and password.
```

6. **Start the Development Server:**
```bash
python manage.py runserver
```

## How to Test the Flow

1. Open your browser to `http://127.0.0.1:8000/`.
2. **Register** a new user as a "Hotel Manager".
3. Navigate to the **Manager Dashboard** and add a new Hotel Property.
4. **Login as Admin** (the superuser you created) at `http://127.0.0.1:8000/admin/`.
   - Go to `Hotels` and edit your new property.
   - Check the `Is approved` box and save.
   - Add `Room Types` (e.g., Deluxe) and individual `Rooms` for that property to allow booking.
5. Create an account as a **Customer** (or logout and browse as guest, login to book).
6. View the hotel, select dates, and proceed to checkout.
7. Upon completing the dummy Stripe process, review your bookings under **My Bookings** and download the PDF invoice.

---
*Built as a professional-grade milestone project.*
