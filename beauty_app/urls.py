from django.urls import path
from beauty_app.views import *

urlpatterns = [
    # --- Existing pages ---
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('services/',services,name='services'),
    path('team/',team,name='team'),
    path('products/',products,name='products'),
    path('gallery/',gallery,name='gallery'),
    path('contact/',contact,name='contact'),

    path('ajax/customer-search/', ajax_customer_search, name='ajax_customer_search'),
    path('booking/',booking,name='booking'),

    # --- AJAX ---
    path('ajax/employees/',get_employees_for_service,name='ajax_employees'),

    # NEW — Customer Auth + Booking History

    path('customer/login/',customer_login,name='customer_login'),
    path('customer/register/',customer_register,name='customer_register'),
    path('customer/logout/',customer_logout,name='customer_logout'),
    path('my-bookings/',booking_history,name='booking_history'),
    
]


