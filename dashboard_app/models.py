from django.db import models
from django.utils import timezone
from datetime import date, datetime
from decimal import Decimal
from django.db.models import Sum

# =========================== ADMIN USER (Super Admin Only) ========================

class AdminUser(models.Model):
    ADMIN_ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
    )
    
    admin_id = models.CharField(max_length=10, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ADMIN_ROLE_CHOICES, default='super_admin')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.admin_id:
            last_admin = AdminUser.objects.all().order_by('id').last()
            if last_admin:
                last_id = int(last_admin.admin_id[3:])
                self.admin_id = f'ADM{str(last_id + 1).zfill(3)}'
            else:
                self.admin_id = 'ADM001'
        super(AdminUser, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.admin_id} - {self.full_name} ({self.role})"


# =========================== EMPLOYEE ========================

class Employee(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    ROLE_CHOICES = (
        ('hair_stylist', 'Hair Stylist'),
        ('senior_stylist', 'Senior Hair Stylist / Creative Stylist'),
        ('hair_colorist', 'Hair Colorist'),
        ('beauty_therapist', 'Beauty Therapist'),
        ('makeup_artist', 'Makeup Artist'),
        ('salon_manager', 'Salon Manager'),
        ('receptionist', 'Front Desk Executive / Receptionist'),
        ('assistant', 'Assistant / Helper'),
    )
    
    employee_id = models.CharField(max_length=10, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, default="9191919191")
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to='employee_profiles/', blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    emergency_contact_relation = models.CharField(max_length=50)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    designation = models.CharField(max_length=100)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=True, null=True)
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    blocked_by = models.ForeignKey(
        'AdminUser', null=True, blank=True,
        on_delete=models.SET_NULL, related_name="blocked_employees"
    )
    blocked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.all().order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id[3:])
                self.employee_id = f'EMP{str(last_id + 1).zfill(3)}'
            else:
                self.employee_id = 'EMP001'
        super(Employee, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.document_name}"


# =========================== VENDOR ========================

class Vendor(models.Model):
    vendor_id = models.CharField(max_length=10, unique=True, editable=False)
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    alternate_mobile = models.CharField(max_length=10, blank=True, null=True)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=True, null=True)
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.vendor_id:
            last_vendor = Vendor.objects.all().order_by('id').last()
            if last_vendor:
                last_id = int(last_vendor.vendor_id[3:])
                self.vendor_id = f'VEN{str(last_id + 1).zfill(3)}'
            else:
                self.vendor_id = 'VEN001'
        super(Vendor, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.vendor_id} - {self.company_name}"


# =========================== PRODUCT ========================

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('hair_care', 'Hair Care Products'),
        ('skin_care', 'Skin Care Products'),
        ('makeup', 'Makeup Products'),
        ('tools', 'Salon Tools & Equipment'),
        ('consumables', 'Consumables'),
        ('other', 'Other'),
    )
    
    product_id = models.CharField(max_length=10, unique=True, editable=False)
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    reorder_level = models.IntegerField(default=10)
    display_on_website = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.product_id:
            last_product = Product.objects.all().order_by('id').last()
            if last_product:
                last_id = int(last_product.product_id[3:])
                self.product_id = f'PRD{str(last_id + 1).zfill(3)}'
            else:
                self.product_id = 'PRD001'
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product_id} - {self.product_name}"
    
    @property
    def total_purchased(self):
        """Total units purchased from all purchase entries"""
        return self.purchases.aggregate(
            total=Sum('quantity_purchased')
        )['total'] or 0

    @property
    def total_new_usage(self):
        """Total units consumed (only 'new' product usage deducts stock)"""
        result = ServiceProductUsage.objects.filter(
            product=self,
            usage_type='new'
        ).aggregate(total=Sum('quantity_used'))['total']
        return float(result) if result else 0

    @property
    def current_stock(self):
        """Net stock = Total Purchased - Total New Usage"""
        return self.total_purchased - self.total_new_usage
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level
    
    @property
    def stock_value(self):
        return self.current_stock * float(self.price)


# =========================== PURCHASE / STOCK ENTRY ========================

class PurchaseEntry(models.Model):
    purchase_id = models.CharField(max_length=10, unique=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    quantity_purchased = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    purchase_date = models.DateField(default=date.today)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_file = models.FileField(upload_to='purchase_invoices/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(
        'AdminUser', on_delete=models.SET_NULL,
        null=True, related_name="purchases_added"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.purchase_id:
            last_purchase = PurchaseEntry.objects.all().order_by('id').last()
            if last_purchase:
                last_id = int(last_purchase.purchase_id[3:])
                self.purchase_id = f'PUR{str(last_id + 1).zfill(3)}'
            else:
                self.purchase_id = 'PUR001'
        try:
            if isinstance(self.quantity_purchased, str):
                self.quantity_purchased = int(self.quantity_purchased)
            if isinstance(self.purchase_price, str):
                self.purchase_price = Decimal(self.purchase_price)
            self.total_amount = Decimal(self.quantity_purchased) * self.purchase_price
        except (ValueError, TypeError) as e:
            print(f"Error calculating total_amount: {e}")
            self.total_amount = Decimal('0.00')
        super(PurchaseEntry, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.purchase_id} - {self.vendor.company_name} - {self.product.product_name}"
    
    class Meta:
        verbose_name_plural = "Purchase Entries"
        ordering = ['-purchase_date', '-id']


# ===========================  SERVICE MANAGEMENT ========================

class Service(models.Model):
    CATEGORY_CHOICES = (
        ('hair_service', 'Hair Services'),
        ('beauty_service', 'Beauty & Skin Care Services'),
        ('makeup_service', 'Makeup Services'),
        ('spa_service', 'Spa & Massage Services'),
        ('nail_service', 'Nail Care Services'),
        ('bridal_service', 'Bridal Packages'),
        ('other', 'Other Services'),
    )
    
    service_id = models.CharField(max_length=10, unique=True, editable=False)
    service_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    display_on_website = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.service_id:
            last_service = Service.objects.all().order_by('id').last()
            if last_service:
                last_id = int(last_service.service_id[3:])
                self.service_id = f'SRV{str(last_id + 1).zfill(3)}'
            else:
                self.service_id = 'SRV001'
        super(Service, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.service_id} - {self.service_name}"
    
    @property
    def available_employees(self):
        return self.service_employees.filter(
            employee__is_active=True,
            employee__is_blocked=False
        )
    
    class Meta:
        ordering = ['category', 'service_name']


# ===========================  SERVICE-EMPLOYEE MAPPING ========================

class ServiceEmployee(models.Model):
    EXPERTISE_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
        ('master', 'Master'),
    )
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_employees')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_services')
    expertise_level = models.CharField(max_length=20, choices=EXPERTISE_CHOICES, default='intermediate')
    custom_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service.service_name} - {self.employee.full_name} ({self.expertise_level})"
    
    @property
    def effective_price(self):
        return self.custom_price if self.custom_price else self.service.base_price
    
    class Meta:
        unique_together = ('service', 'employee')
        ordering = ['-expertise_level', 'employee__full_name']


# ===========================  CUSTOMER MANAGEMENT ========================

class Customer(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    CUSTOMER_TYPE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline (Walk-in)'),
        ('both', 'Both'),
    )
    
    customer_id = models.CharField(max_length=10, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address_line = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, default='offline')
    profile_pic = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='customers_created'
    )
    is_active = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.customer_id:
            last_customer = Customer.objects.all().order_by('id').last()
            if last_customer:
                last_id = int(last_customer.customer_id[3:])
                self.customer_id = f'CUS{str(last_id + 1).zfill(3)}'
            else:
                self.customer_id = 'CUS001'
        super(Customer, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer_id} - {self.full_name} ({self.mobile})"
    
    @property
    def total_appointments(self):
        return self.appointments.count()
    
    @property
    def total_spending(self):
        return self.bills.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    class Meta:
        ordering = ['-registered_on']


# ===========================  APPOINTMENT/BOOKING SYSTEM ========================

class Appointment(models.Model):
    BOOKING_TYPE_CHOICES = (
        ('online', 'Online Booking'),
        ('offline', 'Offline (Walk-in)'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    appointment_id = models.CharField(max_length=10, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='appointments_created'
    )
    special_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.appointment_id:
            last_appointment = Appointment.objects.all().order_by('id').last()
            if last_appointment:
                last_id = int(last_appointment.appointment_id[3:])
                self.appointment_id = f'APT{str(last_id + 1).zfill(3)}'
            else:
                self.appointment_id = 'APT001'
        if self.pk:
            total = self.appointment_services.aggregate(
                total=Sum('service_price')
            )['total'] or Decimal('0.00')
            self.total_amount = total
        super(Appointment, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.appointment_id} - {self.customer.full_name} ({self.appointment_date})"
    
    @property
    def balance_amount(self):
        return self.total_amount - self.advance_paid
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']


# ===========================  APPOINTMENT SERVICES ========================

class AppointmentService(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    STAGE_CHOICES = (
        ('initial', 'Initial Booking'),
        ('additional', 'Additional Service'),
    )
    
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='appointment_services'
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_appointments')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_services')
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    added_at_stage = models.CharField(max_length=15, choices=STAGE_CHOICES, default='initial')
    is_additional = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ✅ NEW: Employee notes/observations during service
    service_notes = models.TextField(
        blank=True, null=True,
        help_text="Employee ke observations - kya kiya, kya discuss hua customer se"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.appointment.appointment_id} - {self.service.service_name} by {self.employee.full_name}"
    
    class Meta:
        ordering = ['added_at']


# ===========================  ✅ NEW: SERVICE PRODUCT USAGE ========================

class ServiceProductUsage(models.Model):
    """
    Track which products were used during a service.
    - 'new' usage = stock se minus hoga
    - 'existing' usage = already open product tha, stock deduct nahi hoga
    """
    
    USAGE_TYPE_CHOICES = (
        ('new', 'New Product Opened'),
        ('existing', 'Existing Product (Already Open)'),
    )
    
    appointment_service = models.ForeignKey(
        AppointmentService,
        on_delete=models.CASCADE,
        related_name='product_usages'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='usage_records'
    )
    usage_type = models.CharField(
        max_length=10,
        choices=USAGE_TYPE_CHOICES,
        default='existing',
        help_text="New = stock deduct hoga | Existing = already open tha, stock nahi katega"
    )
    quantity_used = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1,
        help_text="Kitna use hua (e.g., 1 = 1 bottle, 0.5 = half bottle)"
    )
    notes = models.CharField(
        max_length=300,
        blank=True, null=True,
        help_text="Extra note (e.g., 'Half bottle used', 'Applied twice')"
    )
    recorded_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='product_usages_recorded'
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (
            f"{self.product.product_name} - "
            f"{self.get_usage_type_display()} - "
            f"Qty: {self.quantity_used} - "
            f"By: {self.recorded_by}"
        )
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = "Service Product Usage"
        verbose_name_plural = "Service Product Usages"


# ===========================  BILLING SYSTEM ========================

class Bill(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Debit/Credit Card'),
        ('upi', 'UPI'),
        ('online', 'Online Payment'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
    )
    
    bill_id = models.CharField(max_length=10, unique=True, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='bills')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bills')
    bill_date = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    generated_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL,
        null=True, related_name='bills_generated'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.bill_id:
            last_bill = Bill.objects.all().order_by('id').last()
            if last_bill:
                last_id = int(last_bill.bill_id[3:])
                self.bill_id = f'BIL{str(last_id + 1).zfill(3)}'
            else:
                self.bill_id = 'BIL001'
        self.total_amount = (self.subtotal - self.discount) + self.gst_amount
        if self.amount_paid >= self.total_amount:
            self.payment_status = 'paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'pending'
        super(Bill, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.bill_id} - {self.customer.full_name} - ₹{self.total_amount}"
    
    @property
    def balance_amount(self):
        return self.total_amount - self.amount_paid
    
    class Meta:
        ordering = ['-bill_date']


# ===========================  BILL ITEMS ========================

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='bill_items')
    appointment_service = models.ForeignKey(
        AppointmentService, on_delete=models.CASCADE, related_name='billed_services'
    )
    service_name = models.CharField(max_length=200)
    employee_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super(BillItem, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.bill.bill_id} - {self.service_name} by {self.employee_name}"


