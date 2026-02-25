from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
import json
from dashboard_app.models import *


# HELPER

def get_logged_in_customer(request):
    """Returns logged-in website customer or None."""
    cid = request.session.get('website_customer_id')
    if cid:
        try:
            return Customer.objects.get(pk=cid)
        except Customer.DoesNotExist:
            pass
    return None


# CUSTOMER AUTH — LOGIN

def customer_login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=405)

    mobile   = request.POST.get('mobile', '').strip()
    password = request.POST.get('password', '').strip()

    if not mobile or not password:
        return JsonResponse({'success': False, 'error': 'Mobile aur password zaroori hai.'})

    try:
        customer = Customer.objects.get(mobile=mobile, is_active=True)
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Ye mobile number registered nahi hai.'})

    if not customer.password:
        return JsonResponse({'success': False, 'error': 'Aapka account online registered nahi hai. Pehle sign up karein.'})

    # Plain text password comparison
    if password != customer.password:
        return JsonResponse({'success': False, 'error': 'Password galat hai.'})

    # Set session
    request.session['website_customer_id']     = customer.id
    request.session['website_customer_name']   = customer.full_name
    request.session['website_customer_mobile'] = customer.mobile

    return JsonResponse({
        'success':       True,
        'customer_name': customer.full_name,
        'redirect':      request.POST.get('next', '/'),
    })


# CUSTOMER AUTH — REGISTER

def customer_register(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=405)

    full_name   = request.POST.get('full_name', '').strip()
    mobile      = request.POST.get('mobile', '').strip()
    email       = request.POST.get('email', '').strip()
    password    = request.POST.get('password', '').strip()
    confirm_pwd = request.POST.get('confirm_password', '').strip()

    # Validation
    if not full_name or not mobile or not password:
        return JsonResponse({'success': False, 'error': 'Naam, mobile aur password zaroori hai.'})

    if len(mobile) != 10 or not mobile.isdigit():
        return JsonResponse({'success': False, 'error': 'Mobile number 10 digits ka hona chahiye.'})

    if password != confirm_pwd:
        return JsonResponse({'success': False, 'error': 'Passwords match nahi kar rahe.'})

    if len(password) < 6:
        return JsonResponse({'success': False, 'error': 'Password kam se kam 6 characters ka hona chahiye.'})

    # Check existing
    if Customer.objects.filter(mobile=mobile).exists():
        existing = Customer.objects.get(mobile=mobile)
        if existing.password:
            return JsonResponse({'success': False, 'error': 'Ye mobile number already registered hai. Login karein.'})
        else:
            # Walk-in customer — set password and activate online
            existing.full_name     = full_name
            existing.password      = password  # Plain text
            existing.customer_type = 'both'
            if email:
                existing.email = email
            existing.save()
            customer = existing
    else:
        customer = Customer.objects.create(
            full_name     = full_name,
            mobile        = mobile,
            email         = email or None,
            password      = password,  # Plain text
            customer_type = 'online',
            is_active     = True,
        )

    # Auto login
    request.session['website_customer_id']     = customer.id
    request.session['website_customer_name']   = customer.full_name
    request.session['website_customer_mobile'] = customer.mobile

    return JsonResponse({
        'success':       True,
        'customer_name': customer.full_name,
        'redirect':      '/',
    })


# CUSTOMER AUTH — LOGOUT

def customer_logout(request):
    keys = ['website_customer_id', 'website_customer_name', 'website_customer_mobile']
    for k in keys:
        request.session.pop(k, None)
    return redirect(request.GET.get('next', '/'))


# BOOKING HISTORY (login required)

def booking_history(request):
    customer = get_logged_in_customer(request)
    if not customer:
        return redirect('/?login_required=1')

    appointments = Appointment.objects.filter(
        customer=customer
    ).prefetch_related('appointment_services__service', 'appointment_services__employee').order_by('-appointment_date', '-appointment_time')

    bills = Bill.objects.filter(customer=customer).order_by('-bill_date')

    context = {
        'customer':     customer,
        'appointments': appointments,
        'bills':        bills,
        'customer_logged_in': True,
    }
    return render(request, 'booking_history.html', context)


# HOME PAGE

def home(request):
    services = Service.objects.filter(
        display_on_website=True, is_active=True
    ).order_by('category', 'service_name')[:6]

    team_members = Employee.objects.filter(
        is_active=True, is_blocked=False
    ).exclude(role='receptionist').exclude(role='assistant')[:8]

    products = Product.objects.filter(
        display_on_website=True, is_active=True
    )[:6]

    customer = get_logged_in_customer(request)

    context = {
        'services':     services,
        'team_members': team_members,
        'products':     products,
        'customer':     customer,
        'login_required': request.GET.get('login_required') == '1',
    }
    return render(request, 'home.html', context)


# ABOUT PAGE

def about(request):
    team_members = Employee.objects.filter(
        is_active=True, is_blocked=False
    ).exclude(role__in=['receptionist', 'assistant'])

    context = {
        'team_members': team_members,
        'customer':     get_logged_in_customer(request),
    }
    return render(request, 'about.html', context)


# SERVICES PAGE

def services(request):
    category_param = request.GET.get('category', 'all')
    all_services   = Service.objects.filter(display_on_website=True, is_active=True)
    filtered       = all_services if category_param == 'all' else all_services.filter(category=category_param)

    context = {
        'services':        filtered,
        'categories':      Service.CATEGORY_CHOICES,
        'active_category': category_param,
        'customer':        get_logged_in_customer(request),
    }
    return render(request, 'services.html', context)


# TEAM PAGE

def team(request):
    role_param    = request.GET.get('role', 'all')
    all_employees = Employee.objects.filter(is_active=True, is_blocked=False).exclude(role__in=['receptionist', 'assistant'])
    filtered      = all_employees if role_param == 'all' else all_employees.filter(role=role_param)

    context = {
        'employees':   filtered,
        'roles':       Employee.ROLE_CHOICES,
        'active_role': role_param,
        'customer':    get_logged_in_customer(request),
    }
    return render(request, 'team.html', context)


# PRODUCTS PAGE

def products(request):
    category_param = request.GET.get('category', 'all')
    all_products   = Product.objects.filter(display_on_website=True, is_active=True)
    filtered       = all_products if category_param == 'all' else all_products.filter(category=category_param)

    context = {
        'products':        filtered,
        'categories':      Product.CATEGORY_CHOICES,
        'active_category': category_param,
        'customer':        get_logged_in_customer(request),
    }
    return render(request, 'products.html', context)




# --------------------------- BOOKING PAGE ----------------------------

def ajax_customer_search(request):
    mobile = request.GET.get('mobile', '').strip()
    if not mobile or len(mobile) != 10 or not mobile.isdigit():
        return JsonResponse({'found': False})

    try:
        customer = Customer.objects.get(mobile=mobile)
        return JsonResponse({
            'found': True,
            'customer': {
                'id':     customer.pk,
                'name':   customer.full_name,
                'mobile': customer.mobile,
                'email':  customer.email or '',
                'type':   customer.customer_type,
            }
        })
    except Customer.DoesNotExist:
        return JsonResponse({'found': False})


def booking(request):
    logged_customer = get_logged_in_customer(request)

    services = Service.objects.filter(
        display_on_website=True, is_active=True
    ).order_by('category', 'service_name')

    if request.method == 'POST':
        if not logged_customer:
            return JsonResponse({
                'success': False,
                'error': 'Please login first',
                'login_required': True
            })

        booking_for   = request.POST.get('booking_for', 'myself')   # 'myself' | 'someone'
        customer_type = request.POST.get('customer_type', 'existing') # 'existing' | 'new'
        customer_id   = request.POST.get('customer_id', '').strip()

        full_name  = request.POST.get('full_name', '').strip()
        mobile     = request.POST.get('mobile', '').strip()
        email      = request.POST.get('email', '').strip()

        service_id  = request.POST.get('service_id')
        employee_id = request.POST.get('employee_id')
        apt_date    = request.POST.get('appointment_date')
        apt_time    = request.POST.get('appointment_time')
        advance     = request.POST.get('advance_paid', 0)
        notes       = request.POST.get('special_notes', '')

        # ---- Determine the actual customer ----
        booking_customer = None

        if booking_for == 'myself':
            # Always use logged-in customer
            booking_customer = logged_customer

        elif booking_for == 'someone':
            if customer_type == 'existing' and customer_id:
                # Use found existing customer
                try:
                    booking_customer = Customer.objects.get(pk=customer_id)
                except Customer.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Customer not found.'})

            elif customer_type == 'new':
                # Create new customer (walk-in type, no password)
                if not full_name or not mobile:
                    return JsonResponse({'success': False, 'error': 'Name and mobile are required.'})

                booking_customer, created = Customer.objects.get_or_create(
                    mobile=mobile,
                    defaults={
                        'full_name':     full_name,
                        'email':         email or None,
                        'customer_type': 'offline',
                    }
                )
                # If customer already exists but was not found via search,
                # update name if it was a walk-in without proper name
                if not created and not booking_customer.full_name:
                    booking_customer.full_name = full_name
                    booking_customer.save()
            else:
                return JsonResponse({'success': False, 'error': 'Invalid booking request.'})

        if not booking_customer:
            return JsonResponse({'success': False, 'error': 'Could not determine customer.'})

        # ---- Create the appointment ----
        appointment = Appointment.objects.create(
            customer         = booking_customer,
            booking_type     = 'online',
            appointment_date = apt_date,
            appointment_time = apt_time,
            advance_paid     = float(advance) if advance else 0,
            special_notes    = notes,
            status           = 'pending',
        )

        # ---- Attach service + employee ----
        try:
            service  = Service.objects.get(pk=service_id)
            employee = Employee.objects.get(pk=employee_id)
            try:
                se    = ServiceEmployee.objects.get(service=service, employee=employee)
                price = se.custom_price or service.base_price
            except ServiceEmployee.DoesNotExist:
                price = service.base_price

            AppointmentService.objects.create(
                appointment   = appointment,
                service       = service,
                employee      = employee,
                service_price = price,
            )

            # Update total
            appointment.total_amount = price
            appointment.save()

        except Exception:
            pass

        return JsonResponse({
            'success':        True,
            'appointment_id': appointment.appointment_id,
        })

    # ---- GET ----
    context = {
        'services': services,
        'customer': logged_customer,
    }
    return render(request, 'booking.html', context)


# AJAX: Get employees for a service

@require_GET
def get_employees_for_service(request):
    service_id = request.GET.get('service_id')
    if not service_id:
        return JsonResponse({'employees': []})

    try:
        service           = Service.objects.get(pk=service_id)
        service_employees = ServiceEmployee.objects.filter(
            service=service,
            employee__is_active=True,
            employee__is_blocked=False,
            is_available=True,
        ).select_related('employee')

        data = [{
            'id':          se.employee.id,
            'name':        se.employee.full_name,
            'designation': se.employee.designation,
            'expertise':   se.get_expertise_level_display(),
            'price':       str(se.effective_price),
        } for se in service_employees]

        return JsonResponse({'employees': data, 'base_price': str(service.base_price)})
    except Service.DoesNotExist:
        return JsonResponse({'employees': []})


# GALLERY PAGE

def gallery(request):
    return render(request, 'gallery.html', {'customer': get_logged_in_customer(request)})


# CONTACT PAGE

def contact(request):
    return render(request, 'contact.html', {'customer': get_logged_in_customer(request)})