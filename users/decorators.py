from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def user_is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

def user_is_hotel_manager(user):
    return user.is_authenticated and user.role == 'HOTEL_MANAGER'

def user_is_customer(user):
    return user.is_authenticated and user.role == 'CUSTOMER'

def admin_required(view_func):
    def wrap(request, *args, **kwargs):
        if user_is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def manager_required(view_func):
    def wrap(request, *args, **kwargs):
        if user_is_hotel_manager(request.user) or user_is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def customer_required(view_func):
    def wrap(request, *args, **kwargs):
        if user_is_customer(request.user) or user_is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
