from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q, F, Count, Sum
from datetime import date, datetime, timedelta
from decimal import Decimal

from .models import *
from .decorators import check_blocked_user, login_required, role_required

# ================================================================
# ROLE SUMMARY:
#
# super_admin      → sab kuch
# salon_manager    → customers, appointments, billing, stock_dashboard
# receptionist     → customers, appointments, billing
# hair_stylist     → my_services, update_service_status, record_product_usage
# senior_stylist   → my_services, update_service_status, record_product_usage
# hair_colorist    → my_services, update_service_status, record_product_usage
# beauty_therapist → my_services, update_service_status, record_product_usage
# makeup_artist    → my_services, update_service_status, record_product_usage
# assistant        → my_services only (no status update, no product usage)
# ================================================================

# ================================================================
# AUTH
# ================================================================

def login_view(request):
    if 'user_id' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(username=username, is_active=True)
            if employee.is_blocked:
                messages.error(request,
                    f'Your account has been blocked by {employee.blocked_by.full_name} '
                    f'on {employee.blocked_at.strftime("%Y-%m-%d %H:%M")}. '
                    f'Please contact the administrator.')
                return render(request, 'login.html')
            if password == employee.password:
                request.session['user_id']     = employee.id
                request.session['user_type']   = 'employee'
                request.session['full_name']   = employee.full_name
                request.session['role']        = employee.role
                request.session['email']       = employee.email
                request.session['employee_id'] = employee.employee_id
                messages.success(request, f'Welcome {employee.full_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password!')
                return render(request, 'login.html')
        except Employee.DoesNotExist:
            pass

        try:
            admin = AdminUser.objects.get(username=username, is_active=True)
            if password == admin.password:
                request.session['user_id']   = admin.id
                request.session['user_type'] = 'super_admin'
                request.session['full_name'] = admin.full_name
                request.session['role']      = admin.role
                request.session['email']     = admin.email
                messages.success(request, f'Welcome {admin.full_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password!')
        except AdminUser.DoesNotExist:
            messages.error(request, 'User not found!')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


# ================================================================
# DASHBOARD
# ================================================================

@check_blocked_user
def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first!')
        return redirect('login')

    role      = request.session.get('role')
    user_type = request.session.get('user_type')
    user_id   = request.session.get('user_id')

    user = AdminUser.objects.get(id=user_id) if user_type == 'super_admin' else Employee.objects.get(id=user_id)

    context = {
        'user':              user,
        'role':              role,
        'user_type':         user_type,
        'total_employees':   Employee.objects.filter(is_active=True).count(),
        'total_staff':       Employee.objects.count(),
        'blocked_employees': Employee.objects.filter(is_blocked=True).count(),
        'active_employees':  Employee.objects.filter(is_active=True, is_blocked=False).count(),
    }

    if role == 'super_admin':
        context['total_admins']         = AdminUser.objects.filter(is_active=True).count()
        context['recent_employees']     = Employee.objects.all().order_by('-created_at')[:5]
        context['total_monthly_salary'] = Employee.objects.filter(is_active=True).aggregate(total=Sum('base_salary'))['total'] or 0
        return render(request, 'dashboards/super_admin_dashboard.html', context)

    elif role == 'hair_stylist':
        today = date.today()
        my_services_today = AppointmentService.objects.filter(
            employee=user, appointment__appointment_date=today,
            appointment__status__in=['confirmed', 'in_progress']
        ).select_related('appointment__customer', 'service')
        context['today_appointments']   = my_services_today.count()
        context['completed_today']      = my_services_today.filter(service_status='completed').count()
        context['pending_appointments'] = my_services_today.filter(service_status='pending').count()
        context['my_services_today']    = my_services_today.order_by('appointment__appointment_time')
        return render(request, 'dashboards/hair_stylist_dashboard.html', context)

    elif role == 'senior_stylist':
        today = date.today()
        my_services_today = AppointmentService.objects.filter(
            employee=user, appointment__appointment_date=today,
            appointment__status__in=['confirmed', 'in_progress']
        )
        context['today_appointments'] = my_services_today.count()
        context['team_members']       = Employee.objects.filter(role__in=['hair_stylist', 'assistant'], is_active=True, is_blocked=False).count()
        current_month_start           = datetime(today.year, today.month, 1).date()
        monthly_services              = AppointmentService.objects.filter(employee=user, appointment__appointment_date__gte=current_month_start, service_status='completed')
        context['monthly_revenue']    = sum(s.service_price for s in monthly_services)
        context['my_services_today']  = my_services_today.order_by('appointment__appointment_time')
        return render(request, 'dashboards/senior_stylist_dashboard.html', context)

    elif role == 'hair_colorist':
        today = date.today()
        my_services_today = AppointmentService.objects.filter(
            employee=user, appointment__appointment_date=today,
            appointment__status__in=['confirmed', 'in_progress']
        ).select_related('appointment__customer', 'service')
        context['color_services_today'] = my_services_today.count()
        context['completed_today']      = my_services_today.filter(service_status='completed').count()
        context['pending_services']     = my_services_today.filter(service_status='pending').count()
        context['my_services_today']    = my_services_today.order_by('appointment__appointment_time')
        return render(request, 'dashboards/hair_colorist_dashboard.html', context)

    elif role == 'beauty_therapist':
        today = date.today()
        my_services_today = AppointmentService.objects.filter(
            employee=user, appointment__appointment_date=today,
            appointment__status__in=['confirmed', 'in_progress']
        ).select_related('appointment__customer', 'service')
        context['treatments_today']  = my_services_today.count()
        context['spa_bookings']      = my_services_today.filter(service__category='spa_service').count()
        context['facial_treatments'] = my_services_today.filter(service__category='beauty_service').count()
        context['my_services_today'] = my_services_today.order_by('appointment__appointment_time')
        return render(request, 'dashboards/beauty_therapist_dashboard.html', context)

    elif role == 'makeup_artist':
        today = date.today()
        my_services_today = AppointmentService.objects.filter(
            employee=user, appointment__appointment_date=today,
            appointment__status__in=['confirmed', 'in_progress']
        ).select_related('appointment__customer', 'service')
        context['makeup_sessions_today'] = my_services_today.count()
        context['bridal_bookings']       = my_services_today.filter(service__category='bridal_service').count()
        context['completed_sessions']    = my_services_today.filter(service_status='completed').count()
        context['my_services_today']     = my_services_today.order_by('appointment__appointment_time')
        return render(request, 'dashboards/makeup_artist_dashboard.html', context)

    elif role == 'salon_manager':
        today        = date.today()
        today_bills  = Bill.objects.filter(bill_date__date=today, payment_status__in=['paid', 'partial'])
        all_products = Product.objects.filter(is_active=True)
        context['daily_revenue']    = today_bills.aggregate(total=Sum('total_amount'))['total'] or 0
        context['staff_present']    = Employee.objects.filter(is_active=True, is_blocked=False).count()
        context['customer_visits']  = Appointment.objects.filter(appointment_date=today, status__in=['confirmed', 'in_progress', 'completed']).count()
        context['inventory_alerts'] = sum(1 for p in all_products if p.is_low_stock)
        return render(request, 'dashboards/salon_manager_dashboard.html', context)

    elif role == 'receptionist':
        today = date.today()
        context['walk_ins']               = Appointment.objects.filter(appointment_date=today, booking_type='offline').count()
        context['phone_bookings']         = Appointment.objects.filter(appointment_date=today, booking_type='online').count()
        context['confirmed_appointments'] = Appointment.objects.filter(appointment_date=today, status='confirmed').count()
        context['waiting_customers']      = Appointment.objects.filter(appointment_date=today, status='in_progress').count()
        context['today_appointments']     = Appointment.objects.filter(appointment_date=today).select_related('customer').order_by('appointment_time')[:10]
        return render(request, 'dashboards/receptionist_dashboard.html', context)

    elif role == 'assistant':
        context['tasks_assigned']  = 12
        context['tasks_completed'] = 8
        context['cleaning_tasks']  = 4
        return render(request, 'dashboards/assistant_dashboard.html', context)

    else:
        messages.warning(request, 'Your role is not configured yet. Please contact admin.')
        return render(request, 'dashboard.html', context)


# ================================================================
# EMPLOYEE MANAGEMENT
# Sirf super_admin
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin'])
def add_employee(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                emp = Employee.objects.create(
                    full_name=request.POST.get('full_name'),
                    email=request.POST.get('email'),
                    mobile=request.POST.get('mobile', '9191919191'),
                    dob=request.POST.get('dob'),
                    gender=request.POST.get('gender'),
                    profile_pic=request.FILES.get('profile_pic'),
                    username=request.POST.get('username'),
                    password=request.POST.get('password'),
                    address_line=request.POST.get('address_line'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state'),
                    pincode=request.POST.get('pincode'),
                    emergency_contact_name=request.POST.get('emergency_contact_name'),
                    emergency_contact_number=request.POST.get('emergency_contact_number'),
                    emergency_contact_relation=request.POST.get('emergency_contact_relation'),
                    role=request.POST.get('role'),
                    designation=request.POST.get('designation'),
                    base_salary=request.POST.get('base_salary', 0),
                    account_number=request.POST.get('account_number', ''),
                    ifsc_code=request.POST.get('ifsc_code', ''),
                    account_holder_name=request.POST.get('account_holder_name', ''),
                    bank_name=request.POST.get('bank_name', ''),
                    bank_address=request.POST.get('bank_address', ''),
                    is_active=True
                )
                for name, file in zip(request.POST.getlist('document_name[]'), request.FILES.getlist('documents[]')):
                    if name and file:
                        EmployeeDocument.objects.create(employee=emp, document_name=name, document_file=file)
                messages.success(request, f"✅ Employee {emp.employee_id} - {emp.full_name} added successfully!")
                return redirect("employee_list")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "employee/add_employee.html")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def employee_list(request):
    employees_list = Employee.objects.all().order_by('-id')
    paginator = Paginator(employees_list, 10)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    return render(request, "employee/employee_list.html", {"employees": employees})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def edit_employee(request, id):
    emp = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        emp.full_name   = request.POST.get('full_name')
        emp.email       = request.POST.get('email')
        emp.mobile      = request.POST.get('mobile')
        emp.dob         = request.POST.get('dob')
        emp.gender      = request.POST.get('gender')
        if request.FILES.get('profile_pic'):
            emp.profile_pic = request.FILES.get('profile_pic')
        emp.username = request.POST.get('username')
        new_password = request.POST.get('password')
        if new_password:
            emp.password = new_password
        emp.address_line               = request.POST.get('address_line')
        emp.city                       = request.POST.get('city')
        emp.state                      = request.POST.get('state')
        emp.pincode                    = request.POST.get('pincode')
        emp.emergency_contact_name     = request.POST.get('emergency_contact_name')
        emp.emergency_contact_number   = request.POST.get('emergency_contact_number')
        emp.emergency_contact_relation = request.POST.get('emergency_contact_relation')
        emp.role                 = request.POST.get('role')
        emp.designation          = request.POST.get('designation')
        emp.base_salary          = request.POST.get('base_salary')
        emp.account_number       = request.POST.get('account_number')
        emp.ifsc_code            = request.POST.get('ifsc_code')
        emp.account_holder_name  = request.POST.get('account_holder_name')
        emp.bank_name            = request.POST.get('bank_name')
        emp.bank_address         = request.POST.get('bank_address')
        emp.save()
        for name, file in zip(request.POST.getlist('document_name[]'), request.FILES.getlist('documents[]')):
            if name and file:
                EmployeeDocument.objects.create(employee=emp, document_name=name, document_file=file)
        messages.success(request, f"✅ Employee {emp.employee_id} updated successfully!")
        return redirect("employee_list")
    return render(request, "employee/edit_employee.html", {
        "emp": emp,
        "documents": EmployeeDocument.objects.filter(employee=emp)
    })


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_employee(request, id):
    emp = get_object_or_404(Employee, id=id)
    eid = emp.employee_id
    emp.delete()
    messages.success(request, f"✅ Employee {eid} deleted successfully!")
    return redirect("employee_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_employee_document(request, id):
    doc = get_object_or_404(EmployeeDocument, id=id)
    emp_id = doc.employee.id
    doc.delete()
    messages.success(request, "✅ Document deleted successfully!")
    return redirect("edit_employee", id=emp_id)


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_employee_active(request, id):
    emp = get_object_or_404(Employee, id=id)
    emp.is_active = not emp.is_active
    emp.save()
    status = "activated" if emp.is_active else "deactivated"
    messages.success(request, f"✅ Employee {emp.employee_id} - {emp.full_name} {status} successfully!")
    return redirect("employee_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_employee_block(request, id):
    emp   = get_object_or_404(Employee, id=id)
    admin = AdminUser.objects.get(id=request.session.get('user_id'))
    if emp.is_blocked:
        emp.is_blocked = False
        emp.blocked_by = None
        emp.blocked_at = None
        messages.success(request, f"✅ Employee {emp.employee_id} - {emp.full_name} unblocked successfully!")
    else:
        emp.is_blocked = True
        emp.blocked_by = admin
        emp.blocked_at = datetime.now()
        messages.success(request, f"🚫 Employee {emp.employee_id} - {emp.full_name} blocked successfully!")
    emp.save()
    return redirect("employee_list")


# No role restriction - AJAX utility
def check_email_unique(request):
    email       = request.GET.get('email', '')
    employee_id = request.GET.get('employee_id', None)
    qs = Employee.objects.filter(email=email)
    if employee_id:
        qs = qs.exclude(id=employee_id)
    return JsonResponse({'is_unique': not qs.exists()})


def check_username_unique(request):
    username    = request.GET.get('username', '')
    employee_id = request.GET.get('employee_id', None)
    qs = Employee.objects.filter(username=username)
    if employee_id:
        qs = qs.exclude(id=employee_id)
    return JsonResponse({'is_unique': not qs.exists()})


# ================================================================
# MY SERVICES
# Saare service employees + assistant apni assigned services dekhte hain
# assistant sirf dekh sakta hai, status update/product usage nahi
# ================================================================

@check_blocked_user
@login_required
@role_required(['hair_stylist', 'senior_stylist', 'hair_colorist',
                'beauty_therapist', 'makeup_artist', 'assistant'])
def my_services(request):
    user_id  = request.session.get('user_id')
    employee = Employee.objects.get(id=user_id)
    status_filter = request.GET.get('status')
    date_filter   = request.GET.get('date')

    my_services_list = AppointmentService.objects.filter(
        employee=employee
    ).select_related('appointment__customer', 'service').order_by(
        '-appointment__appointment_date', '-appointment__appointment_time'
    )
    if status_filter:
        my_services_list = my_services_list.filter(service_status=status_filter)
    if date_filter:
        my_services_list = my_services_list.filter(appointment__appointment_date=date_filter)

    paginator = Paginator(my_services_list, 20)
    page = request.GET.get('page')
    try:
        my_services = paginator.page(page)
    except PageNotAnInteger:
        my_services = paginator.page(1)
    except EmptyPage:
        my_services = paginator.page(paginator.num_pages)

    return render(request, 'employee/my_services.html', {
        'employee':       employee,
        'my_services':    my_services,
        'selected_status':status_filter,
        'selected_date':  date_filter,
    })


# ================================================================
# VENDOR MANAGEMENT
# Sirf super_admin
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin'])
def add_vendor(request):
    if request.method == "POST":
        try:
            vendor = Vendor.objects.create(
                company_name=request.POST.get('company_name'),
                contact_person=request.POST.get('contact_person'),
                email=request.POST.get('email'),
                mobile=request.POST.get('mobile'),
                alternate_mobile=request.POST.get('alternate_mobile', ''),
                address_line=request.POST.get('address_line'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                gst_number=request.POST.get('gst_number', ''),
                pan_number=request.POST.get('pan_number', ''),
                account_number=request.POST.get('account_number', ''),
                ifsc_code=request.POST.get('ifsc_code', ''),
                account_holder_name=request.POST.get('account_holder_name', ''),
                bank_name=request.POST.get('bank_name', ''),
                is_active=True
            )
            messages.success(request, f"✅ Vendor {vendor.vendor_id} - {vendor.company_name} added successfully!")
            return redirect("vendor_list")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "vendor/add_vendor.html")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def vendor_list(request):
    vendors_list = Vendor.objects.all().order_by('-id')
    paginator = Paginator(vendors_list, 10)
    page = request.GET.get('page')
    try:
        vendors = paginator.page(page)
    except PageNotAnInteger:
        vendors = paginator.page(1)
    except EmptyPage:
        vendors = paginator.page(paginator.num_pages)
    return render(request, "vendor/vendor_list.html", {"vendors": vendors})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def edit_vendor(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    if request.method == "POST":
        vendor.company_name        = request.POST.get('company_name')
        vendor.contact_person      = request.POST.get('contact_person')
        vendor.email               = request.POST.get('email')
        vendor.mobile              = request.POST.get('mobile')
        vendor.alternate_mobile    = request.POST.get('alternate_mobile')
        vendor.address_line        = request.POST.get('address_line')
        vendor.city                = request.POST.get('city')
        vendor.state               = request.POST.get('state')
        vendor.pincode             = request.POST.get('pincode')
        vendor.gst_number          = request.POST.get('gst_number')
        vendor.pan_number          = request.POST.get('pan_number')
        vendor.account_number      = request.POST.get('account_number')
        vendor.ifsc_code           = request.POST.get('ifsc_code')
        vendor.account_holder_name = request.POST.get('account_holder_name')
        vendor.bank_name           = request.POST.get('bank_name')
        vendor.save()
        messages.success(request, f"✅ Vendor {vendor.vendor_id} - {vendor.company_name} updated successfully!")
        return redirect("vendor_list")
    return render(request, "vendor/edit_vendor.html", {"vendor": vendor})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_vendor(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    vid, name = vendor.vendor_id, vendor.company_name
    vendor.delete()
    messages.success(request, f"✅ Vendor {vid} - {name} deleted successfully!")
    return redirect("vendor_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_vendor_active(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    vendor.is_active = not vendor.is_active
    vendor.save()
    status = "activated" if vendor.is_active else "deactivated"
    messages.success(request, f"✅ Vendor {vendor.vendor_id} - {vendor.company_name} {status} successfully!")
    return redirect("vendor_list")


# ================================================================
# PRODUCT MANAGEMENT
# Sirf super_admin
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin'])
def add_product(request):
    if request.method == "POST":
        try:
            product = Product.objects.create(
                product_name=request.POST.get('product_name'),
                category=request.POST.get('category'),
                brand=request.POST.get('brand', ''),
                price=request.POST.get('price'),
                description=request.POST.get('description'),
                product_image=request.FILES.get('product_image'),
                reorder_level=request.POST.get('reorder_level', 10),
                display_on_website=request.POST.get('display_on_website') == 'on',
                is_active=True
            )
            messages.success(request, f"✅ Product {product.product_id} - {product.product_name} added successfully!")
            return redirect("product_list")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "product/add_product.html")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def product_list(request):
    products_list = Product.objects.all().order_by('-id')
    paginator = Paginator(products_list, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, "product/product_list.html", {"products": products})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.product_name       = request.POST.get('product_name')
        product.category           = request.POST.get('category')
        product.brand              = request.POST.get('brand')
        product.price              = request.POST.get('price')
        product.description        = request.POST.get('description')
        if request.FILES.get('product_image'):
            product.product_image  = request.FILES.get('product_image')
        product.reorder_level      = request.POST.get('reorder_level')
        product.display_on_website = request.POST.get('display_on_website') == 'on'
        product.save()
        messages.success(request, f"✅ Product {product.product_id} - {product.product_name} updated successfully!")
        return redirect("product_list")
    return render(request, "product/edit_product.html", {"product": product})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    pid, name = product.product_id, product.product_name
    product.delete()
    messages.success(request, f"✅ Product {pid} - {name} deleted successfully!")
    return redirect("product_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_product_active(request, id):
    product = get_object_or_404(Product, id=id)
    product.is_active = not product.is_active
    product.save()
    status = "activated" if product.is_active else "deactivated"
    messages.success(request, f"✅ Product {product.product_id} - {product.product_name} {status} successfully!")
    return redirect("product_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_product_display(request, id):
    product = get_object_or_404(Product, id=id)
    product.display_on_website = not product.display_on_website
    product.save()
    status = "visible on website" if product.display_on_website else "hidden from website"
    messages.success(request, f"✅ Product {product.product_id} - {product.product_name} is now {status}!")
    return redirect("product_list")


# ================================================================
# PURCHASE / STOCK MANAGEMENT
# add/edit/delete/history: super_admin only
# stock_dashboard: super_admin + salon_manager (manager ko low stock monitor karna hota hai)
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin'])
def add_purchase(request):
    if request.method == "POST":
        try:
            vendor   = Vendor.objects.get(id=request.POST.get('vendor'))
            product  = Product.objects.get(id=request.POST.get('product'))
            admin    = AdminUser.objects.get(id=request.session.get('user_id'))
            purchase = PurchaseEntry.objects.create(
                vendor=vendor, product=product,
                quantity_purchased=request.POST.get('quantity_purchased'),
                purchase_price=request.POST.get('purchase_price'),
                purchase_date=request.POST.get('purchase_date'),
                invoice_number=request.POST.get('invoice_number', ''),
                invoice_file=request.FILES.get('invoice_file'),
                remarks=request.POST.get('remarks', ''),
                added_by=admin
            )
            messages.success(request, f"✅ Purchase Entry {purchase.purchase_id} added! Current Stock: {product.current_stock} units")
            return redirect("purchase_history")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "purchase/add_purchase.html", {
        'vendors':  Vendor.objects.filter(is_active=True).order_by('company_name'),
        'products': Product.objects.filter(is_active=True).order_by('product_name'),
    })


@check_blocked_user
@login_required
@role_required(['super_admin'])
def purchase_history(request):
    purchases_list  = PurchaseEntry.objects.all().select_related('vendor', 'product', 'added_by').order_by('-purchase_date', '-id')
    vendor_filter   = request.GET.get('vendor')
    product_filter  = request.GET.get('product')
    category_filter = request.GET.get('category')
    date_from       = request.GET.get('date_from')
    date_to         = request.GET.get('date_to')
    if vendor_filter:   purchases_list = purchases_list.filter(vendor_id=vendor_filter)
    if product_filter:  purchases_list = purchases_list.filter(product_id=product_filter)
    if category_filter: purchases_list = purchases_list.filter(product__category=category_filter)
    if date_from:       purchases_list = purchases_list.filter(purchase_date__gte=date_from)
    if date_to:         purchases_list = purchases_list.filter(purchase_date__lte=date_to)
    total_amount   = sum(p.total_amount for p in purchases_list)
    total_quantity = sum(p.quantity_purchased for p in purchases_list)
    paginator = Paginator(purchases_list, 15)
    page = request.GET.get('page')
    try:
        purchases = paginator.page(page)
    except PageNotAnInteger:
        purchases = paginator.page(1)
    except EmptyPage:
        purchases = paginator.page(paginator.num_pages)
    return render(request, "purchase/purchase_history.html", {
        'purchases': purchases,
        'vendors':   Vendor.objects.filter(is_active=True).order_by('company_name'),
        'products':  Product.objects.filter(is_active=True).order_by('product_name'),
        'categories': Product.CATEGORY_CHOICES,
        'total_amount': total_amount, 'total_quantity': total_quantity,
        'selected_vendor': vendor_filter, 'selected_product': product_filter,
        'selected_category': category_filter, 'date_from': date_from, 'date_to': date_to,
    })


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_purchase(request, id):
    purchase = get_object_or_404(PurchaseEntry, id=id)
    pid, name, qty = purchase.purchase_id, purchase.product.product_name, purchase.quantity_purchased
    purchase.delete()
    messages.success(request, f"✅ Purchase {pid} deleted! Stock for {name} reduced by {qty} units.")
    return redirect("purchase_history")


# stock_dashboard: super_admin + salon_manager
@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager'])
def stock_dashboard(request):
    category_filter = request.GET.get('category')
    search_query    = request.GET.get('search')
    show_low_stock  = request.GET.get('low_stock')
    products_list   = Product.objects.filter(is_active=True)
    if category_filter: products_list = products_list.filter(category=category_filter)
    if search_query:    products_list = products_list.filter(
        Q(product_name__icontains=search_query) |
        Q(product_id__icontains=search_query) |
        Q(brand__icontains=search_query)
    )
    if show_low_stock == 'yes':
        products_list = [p for p in products_list if p.is_low_stock]
    else:
        products_list = list(products_list.order_by('category', 'product_name'))
    all_products    = Product.objects.filter(is_active=True)
    category_summary = {}
    for p in all_products:
        cat = p.get_category_display()
        if cat not in category_summary:
            category_summary[cat] = {'product_count': 0, 'total_stock': 0}
        category_summary[cat]['product_count'] += 1
        category_summary[cat]['total_stock']   += p.current_stock
    paginator = Paginator(products_list, 20)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, "purchase/stock_dashboard.html", {
        'products': products, 'categories': Product.CATEGORY_CHOICES,
        'selected_category': category_filter, 'search_query': search_query,
        'show_low_stock': show_low_stock,
        'total_products':    all_products.count(),
        'low_stock_count':   sum(1 for p in all_products if p.is_low_stock),
        'out_of_stock':      sum(1 for p in all_products if p.current_stock == 0),
        'total_stock_value': sum(p.stock_value for p in all_products),
        'category_summary':  category_summary.items(),
    })


# AJAX - login required only (form ke andar use hota hai)
@check_blocked_user
@login_required
def get_products_by_category(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category, is_active=True)
        return JsonResponse({'products': [{
            'id': p.id, 'product_id': p.product_id, 'product_name': p.product_name,
            'brand': p.brand or '', 'current_stock': p.current_stock,
            'reorder_level': p.reorder_level, 'is_low_stock': p.is_low_stock,
        } for p in products]})
    return JsonResponse({'products': []})


# ================================================================
# SERVICE MANAGEMENT
# add/edit/delete/assign: super_admin only
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin'])
def add_service(request):
    if request.method == "POST":
        try:
            service = Service.objects.create(
                service_name=request.POST.get('service_name'),
                category=request.POST.get('category'),
                description=request.POST.get('description'),
                duration_minutes=request.POST.get('duration_minutes'),
                base_price=request.POST.get('base_price'),
                service_image=request.FILES.get('service_image'),
                display_on_website=request.POST.get('display_on_website') == 'on',
                is_active=True
            )
            messages.success(request, f"✅ Service {service.service_id} - {service.service_name} added successfully!")
            return redirect("service_list")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "service/add_service.html")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def service_list(request):
    services_list   = Service.objects.all().order_by('-id')
    category_filter = request.GET.get('category')
    search_query    = request.GET.get('search')
    if category_filter: services_list = services_list.filter(category=category_filter)
    if search_query:    services_list = services_list.filter(
        Q(service_name__icontains=search_query) | Q(service_id__icontains=search_query)
    )
    paginator = Paginator(services_list, 10)
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)
    return render(request, "service/service_list.html", {
        'services': services, 'categories': Service.CATEGORY_CHOICES,
        'selected_category': category_filter, 'search_query': search_query,
    })


@check_blocked_user
@login_required
@role_required(['super_admin'])
def edit_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == "POST":
        service.service_name     = request.POST.get('service_name')
        service.category         = request.POST.get('category')
        service.description      = request.POST.get('description')
        service.duration_minutes = request.POST.get('duration_minutes')
        service.base_price       = request.POST.get('base_price')
        if request.FILES.get('service_image'):
            service.service_image = request.FILES.get('service_image')
        service.display_on_website = request.POST.get('display_on_website') == 'on'
        service.save()
        messages.success(request, f"✅ Service {service.service_id} - {service.service_name} updated successfully!")
        return redirect("service_list")
    return render(request, "service/edit_service.html", {"service": service})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    sid, name = service.service_id, service.service_name
    service.delete()
    messages.success(request, f"✅ Service {sid} - {name} deleted successfully!")
    return redirect("service_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_service_active(request, id):
    service = get_object_or_404(Service, id=id)
    service.is_active = not service.is_active
    service.save()
    status = "activated" if service.is_active else "deactivated"
    messages.success(request, f"✅ Service {service.service_id} - {service.service_name} {status} successfully!")
    return redirect("service_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_service_display(request, id):
    service = get_object_or_404(Service, id=id)
    service.display_on_website = not service.display_on_website
    service.save()
    status = "visible on website" if service.display_on_website else "hidden from website"
    messages.success(request, f"✅ Service {service.service_id} - {service.service_name} is now {status}!")
    return redirect("service_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def assign_service_to_employee(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        try:
            employee_ids = request.POST.getlist('employees[]')
            for emp_id in employee_ids:
                employee     = Employee.objects.get(id=emp_id)
                expertise    = request.POST.get(f'expertise_{emp_id}', 'intermediate')
                custom_price = request.POST.get(f'custom_price_{emp_id}', None)
                service_emp, created = ServiceEmployee.objects.get_or_create(
                    service=service, employee=employee,
                    defaults={'expertise_level': expertise, 'custom_price': custom_price if custom_price else None, 'is_available': True}
                )
                if not created:
                    service_emp.expertise_level = expertise
                    service_emp.custom_price    = custom_price if custom_price else None
                    service_emp.is_available    = True
                    service_emp.save()
            messages.success(request, f"✅ Service '{service.service_name}' assigned to {len(employee_ids)} employee(s) successfully!")
            return redirect("manage_service_employees", service_id=service_id)
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    assigned_ids = ServiceEmployee.objects.filter(service=service).values_list('employee_id', flat=True)
    return render(request, "service/assign_service_to_employee.html", {
        'service': service,
        'available_employees': Employee.objects.filter(is_active=True, is_blocked=False).exclude(id__in=assigned_ids).order_by('full_name'),
    })


@check_blocked_user
@login_required
@role_required(['super_admin'])
def manage_service_employees(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, "service/manage_service_employees.html", {
        'service': service,
        'service_employees': ServiceEmployee.objects.filter(service=service).select_related('employee').order_by('-expertise_level', 'employee__full_name'),
    })


@check_blocked_user
@login_required
@role_required(['super_admin'])
def remove_employee_from_service(request, service_employee_id):
    service_emp = get_object_or_404(ServiceEmployee, id=service_employee_id)
    service_id  = service_emp.service.id
    messages.success(request, f"✅ {service_emp.employee.full_name} removed from '{service_emp.service.service_name}' successfully!")
    service_emp.delete()
    return redirect("manage_service_employees", service_id=service_id)


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_service_employee_availability(request, service_employee_id):
    service_emp = get_object_or_404(ServiceEmployee, id=service_employee_id)
    service_emp.is_available = not service_emp.is_available
    service_emp.save()
    status = "available" if service_emp.is_available else "unavailable"
    messages.success(request, f"✅ {service_emp.employee.full_name} is now {status} for '{service_emp.service.service_name}'!")
    return redirect("manage_service_employees", service_id=service_emp.service.id)


# CUSTOMER MANAGEMENT
@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def add_customer(request):
    if request.method == "POST":
        try:
            user_type  = request.session.get('user_type')
            created_by = None if user_type == 'super_admin' else Employee.objects.get(id=request.session.get('user_id'))
            dob        = request.POST.get('dob', None)
            customer   = Customer.objects.create(
                full_name=request.POST.get('full_name'),
                mobile=request.POST.get('mobile'),
                email=request.POST.get('email', '') or None,
                gender=request.POST.get('gender', '') or None,
                dob=dob if dob else None,
                address_line=request.POST.get('address_line', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                pincode=request.POST.get('pincode', ''),
                profile_pic=request.FILES.get('profile_pic'),
                customer_type='offline',
                created_by=created_by,
                is_active=True
            )
            messages.success(request, f"✅ Customer {customer.customer_id} - {customer.full_name} added successfully!")
            return redirect("create_appointment", customer_id=customer.id)
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "customer/add_customer.html")


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def customer_list(request):
    customers_list       = Customer.objects.all().order_by('-registered_on')
    customer_type_filter = request.GET.get('customer_type')
    search_query         = request.GET.get('search')
    if customer_type_filter: customers_list = customers_list.filter(customer_type=customer_type_filter)
    if search_query:         customers_list = customers_list.filter(
        Q(full_name__icontains=search_query) | Q(customer_id__icontains=search_query) |
        Q(mobile__icontains=search_query)    | Q(email__icontains=search_query)
    )
    paginator = Paginator(customers_list, 15)
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)
    return render(request, "customer/customer_list.html", {
        'customers': customers, 'customer_types': Customer.CUSTOMER_TYPE_CHOICES,
        'selected_type': customer_type_filter, 'search_query': search_query,
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def view_customer(request, id):
    customer     = get_object_or_404(Customer, id=id)
    appointments = Appointment.objects.filter(customer=customer).order_by('-appointment_date', '-appointment_time')
    bills        = Bill.objects.filter(customer=customer).order_by('-bill_date')
    return render(request, "customer/view_customer.html", {
        'customer':               customer,
        'appointments':           appointments[:10],
        'bills':                  bills[:10],
        'total_appointments':     appointments.count(),
        'completed_appointments': appointments.filter(status='completed').count(),
        'cancelled_appointments': appointments.filter(status='cancelled').count(),
        'total_spending':         customer.total_spending,
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == "POST":
        customer.full_name    = request.POST.get('full_name')
        customer.mobile       = request.POST.get('mobile')
        customer.email        = request.POST.get('email', '')
        customer.gender       = request.POST.get('gender', '')
        dob                   = request.POST.get('dob', '')
        customer.dob          = dob if dob else None
        customer.address_line = request.POST.get('address_line', '')
        customer.city         = request.POST.get('city', '')
        customer.state        = request.POST.get('state', '')
        customer.pincode      = request.POST.get('pincode', '')
        if request.FILES.get('profile_pic'):
            customer.profile_pic = request.FILES.get('profile_pic')
        customer.save()
        messages.success(request, f"✅ Customer {customer.customer_id} - {customer.full_name} updated successfully!")
        return redirect("customer_list")
    return render(request, "customer/edit_customer.html", {"customer": customer})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    cid, name = customer.customer_id, customer.full_name
    customer.delete()
    messages.success(request, f"✅ Customer {cid} - {name} deleted successfully!")
    return redirect("customer_list")


@check_blocked_user
@login_required
@role_required(['super_admin'])
def toggle_customer_active(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.is_active = not customer.is_active
    customer.save()
    status = "activated" if customer.is_active else "deactivated"
    messages.success(request, f"✅ Customer {customer.customer_id} - {customer.full_name} {status} successfully!")
    return redirect("customer_list")


# ================================================================
# APPOINTMENT MANAGEMENT
# create/list/view/edit/cancel/add_additional: super_admin + salon_manager + receptionist
# update_service_status: service staff (hair_stylist, senior_stylist, hair_colorist,
#                         beauty_therapist, makeup_artist) + super_admin
# record_product_usage:  same as above
# view_product_usage:    super_admin + salon_manager only
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def create_appointment(request, customer_id=None):
    selected_customer = get_object_or_404(Customer, id=customer_id) if customer_id else None
    if request.method == "POST":
        try:
            with transaction.atomic():
                customer     = Customer.objects.get(id=request.POST.get('customer_id'))
                user_type    = request.session.get('user_type')
                created_by   = None if user_type == 'super_admin' else Employee.objects.get(id=request.session.get('user_id'))
                appointment  = Appointment.objects.create(
                    customer=customer,
                    booking_type='offline',
                    appointment_date=request.POST.get('appointment_date'),
                    appointment_time=request.POST.get('appointment_time'),
                    status='confirmed',
                    advance_paid=request.POST.get('advance_paid', 0) or 0,
                    special_notes=request.POST.get('special_notes', ''),
                    created_by=created_by
                )
                service_ids  = request.POST.getlist('service_ids[]')
                employee_ids = request.POST.getlist('employee_ids[]')
                total_amount = Decimal('0.00')
                for service_id, employee_id in zip(service_ids, employee_ids):
                    service  = Service.objects.get(id=service_id)
                    employee = Employee.objects.get(id=employee_id)
                    try:
                        service_emp   = ServiceEmployee.objects.get(service=service, employee=employee)
                        service_price = service_emp.effective_price
                    except ServiceEmployee.DoesNotExist:
                        service_price = service.base_price
                    AppointmentService.objects.create(
                        appointment=appointment, service=service, employee=employee,
                        service_price=service_price, service_status='pending',
                        added_at_stage='initial', is_additional=False
                    )
                    total_amount += service_price
                appointment.total_amount = total_amount
                appointment.save()
                messages.success(request, f"✅ Appointment {appointment.appointment_id} created successfully for {customer.full_name}!")
                return redirect("appointment_list")
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "appointment/create_appointment.html", {
        'customers':         Customer.objects.filter(is_active=True).order_by('full_name'),
        'categories':        Service.CATEGORY_CHOICES,
        'selected_customer': selected_customer,
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def appointment_list(request):
    appointments_list   = Appointment.objects.all().select_related('customer', 'created_by').order_by('-appointment_date', '-appointment_time')
    status_filter       = request.GET.get('status')
    booking_type_filter = request.GET.get('booking_type')
    date_filter         = request.GET.get('date')
    search_query        = request.GET.get('search')
    if status_filter:       appointments_list = appointments_list.filter(status=status_filter)
    if booking_type_filter: appointments_list = appointments_list.filter(booking_type=booking_type_filter)
    if date_filter:         appointments_list = appointments_list.filter(appointment_date=date_filter)
    if search_query:        appointments_list = appointments_list.filter(
        Q(appointment_id__icontains=search_query) |
        Q(customer__full_name__icontains=search_query) |
        Q(customer__mobile__icontains=search_query)
    )
    today = date.today()
    paginator = Paginator(appointments_list, 15)
    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    return render(request, "appointment/appointment_list.html", {
        'appointments':           appointments,
        'statuses':               Appointment.STATUS_CHOICES,
        'booking_types':          Appointment.BOOKING_TYPE_CHOICES,
        'selected_status':        status_filter,
        'selected_booking_type':  booking_type_filter,
        'selected_date':          date_filter,
        'search_query':           search_query,
        'today_appointments':     Appointment.objects.filter(appointment_date=today).count(),
        'pending_appointments':   Appointment.objects.filter(status='pending').count(),
        'confirmed_appointments': Appointment.objects.filter(status='confirmed').count(),
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def view_appointment(request, id):
    appointment          = get_object_or_404(Appointment, id=id)
    appointment_services = AppointmentService.objects.filter(appointment=appointment).select_related('service', 'employee').order_by('added_at')
    return render(request, "appointment/view_appointment.html", {
        'appointment':         appointment,
        'initial_services':    appointment_services.filter(is_additional=False),
        'additional_services': appointment_services.filter(is_additional=True),
        'all_services':        appointment_services,
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.appointment_time = request.POST.get('appointment_time')
        appointment.status           = request.POST.get('status')
        appointment.special_notes    = request.POST.get('special_notes', '')
        appointment.advance_paid     = request.POST.get('advance_paid', 0)
        appointment.save()
        messages.success(request, f"✅ Appointment {appointment.appointment_id} updated successfully!")
        return redirect("appointment_list")
    return render(request, "appointment/edit_appointment.html", {'appointment': appointment})


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def add_additional_service(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        try:
            with transaction.atomic():
                service  = Service.objects.get(id=request.POST.get('service_id'))
                employee = Employee.objects.get(id=request.POST.get('employee_id'))
                try:
                    service_emp   = ServiceEmployee.objects.get(service=service, employee=employee)
                    service_price = service_emp.effective_price
                except ServiceEmployee.DoesNotExist:
                    service_price = service.base_price
                AppointmentService.objects.create(
                    appointment=appointment, service=service, employee=employee,
                    service_price=service_price, service_status='pending',
                    added_at_stage='additional', is_additional=True
                )
                appointment.save()
                messages.success(request, f"✅ Additional service '{service.service_name}' added to appointment {appointment.appointment_id}!")
                return redirect("view_appointment", id=appointment_id)
        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())
    return render(request, "appointment/add_additional_service.html", {
        'appointment': appointment,
        'services':    Service.objects.filter(is_active=True).order_by('category', 'service_name'),
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, f"✅ Appointment {appointment.appointment_id} cancelled successfully!")
    return redirect("appointment_list")


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def update_appointment_status(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    new_status  = request.GET.get('status')
    if new_status in dict(Appointment.STATUS_CHOICES):
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"✅ Appointment status updated to '{appointment.get_status_display()}'!")
    else:
        messages.error(request, "❌ Invalid status!")
    return redirect("appointment_list")


# update_service_status: service staff + super_admin
# assistant excluded - wo sirf dekh sakta hai, status update nahi kar sakta
@check_blocked_user
@login_required
@role_required(['super_admin', 'hair_stylist', 'senior_stylist',
                'hair_colorist', 'beauty_therapist', 'makeup_artist'])
def update_service_status(request, service_id):
    appointment_service = get_object_or_404(AppointmentService, id=service_id)
    user_id   = request.session.get('user_id')
    user_type = request.session.get('user_type')

    # Employee sirf apni service update kar sakta hai
    if user_type == 'employee':
        employee = Employee.objects.get(id=user_id)
        if appointment_service.employee != employee:
            messages.error(request, "❌ You are not authorized to update this service!")
            return redirect("dashboard")

    new_status = request.GET.get('status')

    if new_status == 'in_progress':
        appointment_service.service_status = 'in_progress'
        appointment = appointment_service.appointment
        if appointment.status == 'confirmed':
            appointment.status = 'in_progress'
            appointment.save()
        appointment_service.save()
        messages.success(request, "✅ Service started!")
        return redirect("dashboard")

    elif new_status == 'completed':
        return redirect("record_product_usage", service_id=service_id)

    messages.error(request, "❌ Invalid status!")
    return redirect("dashboard")


# record_product_usage: service staff + super_admin
# assistant excluded
@check_blocked_user
@login_required
@role_required(['super_admin', 'hair_stylist', 'senior_stylist',
                'hair_colorist', 'beauty_therapist', 'makeup_artist'])
def record_product_usage(request, service_id):
    appointment_service = get_object_or_404(AppointmentService, id=service_id)
    user_id   = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type == 'employee':
        employee = Employee.objects.get(id=user_id)
        if appointment_service.employee != employee:
            messages.error(request, "❌ Not authorized!")
            return redirect("dashboard")
    else:
        employee = None  # super_admin

    if appointment_service.service_status == 'completed':
        messages.warning(request, "⚠️ This service is already completed.")
        return redirect("dashboard")

    if request.method == "POST":
        with transaction.atomic():
            appointment_service.service_notes = request.POST.get('service_notes', '')
            product_ids = request.POST.getlist('product_id[]')
            usage_types = request.POST.getlist('usage_type[]')
            quantities  = request.POST.getlist('quantity[]')
            notes_list  = request.POST.getlist('product_notes[]')

            for i, product_id in enumerate(product_ids):
                if product_id:
                    try:
                        product    = Product.objects.get(id=product_id)
                        usage_type = usage_types[i] if i < len(usage_types) else 'existing'
                        quantity   = float(quantities[i]) if i < len(quantities) and quantities[i] else 1.0
                        note       = notes_list[i] if i < len(notes_list) else ''
                        ServiceProductUsage.objects.create(
                            appointment_service=appointment_service,
                            product=product, usage_type=usage_type,
                            quantity_used=quantity, notes=note,
                            recorded_by=employee
                        )
                    except Product.DoesNotExist:
                        continue

            appointment_service.service_status = 'completed'
            appointment_service.completed_at   = datetime.now()
            appointment_service.save()

            appointment   = appointment_service.appointment
            all_services  = AppointmentService.objects.filter(appointment=appointment)
            all_completed = all(s.service_status == 'completed' for s in all_services)

            if all_completed:
                appointment.status = 'completed'
                appointment.save()
                messages.success(request, f"✅ Sab services complete! Appointment {appointment.appointment_id} completed.")
                if user_type == 'super_admin':
                    return redirect("generate_bill", appointment_id=appointment.id)
                emp_role = Employee.objects.get(id=user_id).role if user_type == 'employee' else None
                if emp_role in ['salon_manager', 'receptionist']:
                    return redirect("generate_bill", appointment_id=appointment.id)
                messages.info(request, "ℹ️ Please ask receptionist to generate the bill.")
                return redirect("dashboard")
            else:
                remaining = all_services.filter(service_status__in=['pending', 'in_progress']).count()
                messages.success(request, f"✅ Service complete! {remaining} service(s) abhi baaki hain.")
                return redirect("dashboard")

    service_category = appointment_service.service.category
    CATEGORY_PRODUCT_MAP = {
        'hair_service':   ['hair_care', 'consumables'],
        'beauty_service': ['skin_care', 'consumables'],
        'makeup_service': ['makeup', 'consumables'],
        'spa_service':    ['skin_care', 'consumables'],
        'nail_service':   ['consumables', 'other'],
        'bridal_service': ['makeup', 'hair_care', 'skin_care', 'consumables'],
        'other':          ['consumables', 'other'],
    }
    relevant_categories = CATEGORY_PRODUCT_MAP.get(service_category, ['consumables', 'other'])
    return render(request, 'appointment/record_product_usage.html', {
        'appointment_service': appointment_service,
        'appointment':         appointment_service.appointment,
        'suggested_products':  Product.objects.filter(is_active=True, category__in=relevant_categories).order_by('product_name'),
        'all_products':        Product.objects.filter(is_active=True).order_by('category', 'product_name'),
        'existing_usages':     ServiceProductUsage.objects.filter(appointment_service=appointment_service),
    })


# view_product_usage: super_admin + salon_manager only
@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'hair_stylist', 'senior_stylist', 
                'hair_colorist', 'beauty_therapist', 'makeup_artist', 'assistant', 'receptionist'])
def view_product_usage(request, service_id):
    appointment_service = get_object_or_404(AppointmentService, id=service_id)
    
    # Employee sirf apni service dekh sake
    user_type = request.session.get('user_type')
    if user_type == 'employee':
        employee = Employee.objects.get(id=request.session.get('user_id'))
        if appointment_service.employee != employee:
            messages.error(request, "❌ Ye service tumhari nahi hai!")
            return redirect('dashboard')
    
    return render(request, 'appointment/view_product_usage.html', {
        'appointment_service': appointment_service,
        'usages': ServiceProductUsage.objects.filter(
            appointment_service=appointment_service
        ).select_related('product', 'recorded_by'),
    })


# AJAX ENDPOINTS
# Login required, no strict role restriction (forms mein use hota hai)

@check_blocked_user
@login_required
def get_employees_for_service(request):
    service_id = request.GET.get('service_id')
    if service_id:
        service = Service.objects.get(id=service_id)
        service_employees = ServiceEmployee.objects.filter(
            service=service, is_available=True,
            employee__is_active=True, employee__is_blocked=False
        ).select_related('employee')
        return JsonResponse({
            'employees': [{
                'id':          se.employee.id,
                'employee_id': se.employee.employee_id,
                'full_name':   se.employee.full_name,
                'expertise':   se.get_expertise_level_display(),
                'price':       str(se.effective_price),
            } for se in service_employees],
            'base_price': str(service.base_price)
        })
    return JsonResponse({'employees': [], 'base_price': '0.00'})


@check_blocked_user
@login_required
def get_services_by_category(request):
    category = request.GET.get('category')
    if category:
        services = Service.objects.filter(category=category, is_active=True).order_by('service_name')
        return JsonResponse({'services': [{
            'id':               s.id,
            'service_name':     s.service_name,
            'base_price':       str(s.base_price),
            'duration_minutes': s.duration_minutes,
        } for s in services]})
    return JsonResponse({'services': []})


@check_blocked_user
@login_required
def search_customers(request):
    query = request.GET.get('q', '')
    if len(query) >= 2:
        customers = Customer.objects.filter(
            Q(full_name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(customer_id__icontains=query)
        ).filter(is_active=True)[:10]
        return JsonResponse({'customers': [{
            'id':          c.id,
            'customer_id': c.customer_id,
            'full_name':   c.full_name,
            'mobile':      c.mobile,
            'email':       c.email or '',
        } for c in customers]})
    return JsonResponse({'customers': []})


# ================================================================
# BILLING SYSTEM
# generate/list/update_payment: super_admin + salon_manager + receptionist
# view_bill: sab logged-in users (employee bhi apna bill print kar sake)
# delete_bill: super_admin only
# ================================================================

@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def generate_bill(request, appointment_id):
    appointment   = get_object_or_404(Appointment, id=appointment_id)
    existing_bill = Bill.objects.filter(appointment=appointment).first()
    if existing_bill:
        messages.warning(request, "Bill already exists for this appointment!")
        return redirect("view_bill", id=existing_bill.id)

    advance_paid = appointment.advance_paid  # Appointment ke time jo advance liya tha

    if request.method == "POST":
        try:
            with transaction.atomic():
                discount        = Decimal(str(request.POST.get('discount', 0) or 0))
                gst_percentage  = Decimal(str(request.POST.get('gst_percentage', 0) or 0))
                payment_method  = request.POST.get('payment_method', 'cash')
                additional_paid = Decimal(str(request.POST.get('amount_paid', 0) or 0))
                notes           = request.POST.get('notes', '')

                app_services = AppointmentService.objects.filter(appointment=appointment)
                subtotal     = sum(s.service_price for s in app_services)

                gst_amount   = (subtotal - discount) * gst_percentage / 100

                # Total amount paid = advance (already collected) + additional payment at billing time
                total_amount_paid = advance_paid + additional_paid

                user_type    = request.session.get('user_type')
                generated_by = None if user_type == 'super_admin' else Employee.objects.get(
                    id=request.session.get('user_id')
                )

                bill = Bill.objects.create(
                    appointment    = appointment,
                    customer       = appointment.customer,
                    subtotal       = subtotal,
                    discount       = discount,
                    gst_amount     = gst_amount,
                    payment_method = payment_method,
                    amount_paid    = total_amount_paid,  # advance + additional
                    notes          = notes,
                    generated_by   = generated_by
                )

                for app_service in app_services:
                    BillItem.objects.create(
                        bill                = bill,
                        appointment_service = app_service,
                        service_name        = app_service.service.service_name,
                        employee_name       = app_service.employee.full_name,
                        quantity            = 1,
                        price               = app_service.service_price
                    )

                if bill.payment_status == 'paid':
                    appointment.status = 'completed'
                    appointment.save()

                messages.success(request, f"✅ Bill {bill.bill_id} generated successfully!")
                return redirect("view_bill", id=bill.id)

        except Exception as e:
            messages.error(request, f"❌ Error: {str(e)}")
            import traceback; print(traceback.format_exc())

    app_services = AppointmentService.objects.filter(appointment=appointment).select_related('service', 'employee')
    subtotal     = sum(s.service_price for s in app_services)

    return render(request, "billing/generate_bill.html", {
        'appointment':          appointment,
        'appointment_services': app_services,
        'subtotal':             subtotal,
        'advance_paid':         advance_paid,   # Template ko bhejo
    })


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def bill_list(request):
    bills_list            = Bill.objects.all().select_related('customer', 'appointment', 'generated_by').order_by('-bill_date')
    payment_status_filter = request.GET.get('payment_status')
    payment_method_filter = request.GET.get('payment_method')
    date_from             = request.GET.get('date_from')
    date_to               = request.GET.get('date_to')
    search_query          = request.GET.get('search')
    if payment_status_filter: bills_list = bills_list.filter(payment_status=payment_status_filter)
    if payment_method_filter: bills_list = bills_list.filter(payment_method=payment_method_filter)
    if date_from:             bills_list = bills_list.filter(bill_date__gte=date_from)
    if date_to:               bills_list = bills_list.filter(bill_date__lte=date_to)
    if search_query:          bills_list = bills_list.filter(
        Q(bill_id__icontains=search_query) |
        Q(customer__full_name__icontains=search_query) |
        Q(customer__mobile__icontains=search_query)
    )
    paginator = Paginator(bills_list, 15)
    page = request.GET.get('page')
    try:
        bills = paginator.page(page)
    except PageNotAnInteger:
        bills = paginator.page(1)
    except EmptyPage:
        bills = paginator.page(paginator.num_pages)
    return render(request, "billing/bill_list.html", {
        'bills': bills,
        'payment_statuses':        Bill.PAYMENT_STATUS_CHOICES,
        'payment_methods':         Bill.PAYMENT_METHOD_CHOICES,
        'selected_payment_status': payment_status_filter,
        'selected_payment_method': payment_method_filter,
        'date_from': date_from, 'date_to': date_to, 'search_query': search_query,
        'total_revenue': bills_list.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00'),
        'total_paid':    bills_list.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00'),
        'total_pending': bills_list.filter(payment_status='pending').aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00'),
    })


# view_bill: sab log dekh sakte hain (employee bhi)
@check_blocked_user
@login_required
def view_bill(request, id):
    bill       = get_object_or_404(Bill, id=id)
    bill_items = BillItem.objects.filter(bill=bill).select_related(
        'appointment_service__service', 'appointment_service__employee'
    )
    return render(request, "billing/view_bill.html", {'bill': bill, 'bill_items': bill_items})


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def update_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == "POST":
        bill.amount_paid   += Decimal(str(request.POST.get('additional_payment', 0)))
        bill.payment_method = request.POST.get('payment_method', bill.payment_method)
        bill.save()
        messages.success(request, f"✅ Payment updated! Amount paid: ₹{bill.amount_paid}, Balance: ₹{bill.balance_amount}")
        return redirect("view_bill", id=bill_id)
    return render(request, "billing/update_payment.html", {'bill': bill})


@check_blocked_user
@login_required
@role_required(['super_admin', 'salon_manager', 'receptionist'])
def print_bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    bill_items = BillItem.objects.filter(bill=bill).select_related(
        'appointment_service__service', 'appointment_service__employee'
    )
    return render(request, "billing/print_bill.html", {'bill': bill, 'bill_items': bill_items})


@check_blocked_user
@login_required
@role_required(['super_admin'])
def delete_bill(request, id):
    bill    = get_object_or_404(Bill, id=id)
    bill_id = bill.bill_id
    bill.delete()
    messages.success(request, f"✅ Bill {bill_id} deleted successfully!")
    return redirect("bill_list")


