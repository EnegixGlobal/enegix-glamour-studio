from django.urls import path
from .views import*

urlpatterns = [

    path('',   login_view, name='login'),
    path('login/',   login_view, name='login'),
    path('logout/',   logout_view, name='logout'),
    path('dashboard/',   dashboard, name='dashboard'),

    # ------------------------ Employee --------------------------

    path('employee/add/', add_employee, name='add_employee'),
    path('employee/list/', employee_list, name='employee_list'),
    path('employee/edit/<int:id>/', edit_employee, name='edit_employee'),
    path('employee/delete/<int:id>/', delete_employee, name='delete_employee'),
    path('employee/toggle-active/<int:id>/', toggle_employee_active, name='toggle_employee_active'),
    path('employee/toggle-block/<int:id>/', toggle_employee_block, name='toggle_employee_block'),
    path('employee/document/delete/<int:id>/', delete_employee_document, name='delete_employee_document'),

    path('check-email-unique/',   check_email_unique, name='check_email_unique'),
    path('check-username-unique/',   check_username_unique, name='check_username_unique'),



    path('employee/my-services/',  my_services, name='my_services'),


     
    # ---------------------- VENDOR URLs ----------------------

    path('add-vendor/', add_vendor, name='add_vendor'),
    path('vendor-list/', vendor_list, name='vendor_list'),
    path('edit-vendor/<int:id>/', edit_vendor, name='edit_vendor'),
    path('delete-vendor/<int:id>/', delete_vendor, name='delete_vendor'),
    path('toggle-vendor-active/<int:id>/', toggle_vendor_active, name='toggle_vendor_active'),
    
    # ---------------------- PRODUCT URLs ----------------------

    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/', delete_product, name='delete_product'),
    path('toggle-product-active/<int:id>/', toggle_product_active, name='toggle_product_active'),
    path('toggle-product-display/<int:id>/', toggle_product_display, name='toggle_product_display'),


    # ======================= PURCHASE / STOCK MANAGEMENT ======================
    path('purchase/add/', add_purchase, name='add_purchase'),
    path('purchase/history/', purchase_history, name='purchase_history'),
    path('purchase/delete/<int:id>/', delete_purchase, name='delete_purchase'),
    path('stock/dashboard/', stock_dashboard, name='stock_dashboard'),
    
    # AJAX endpoint for dynamic product loading
    path('get-products-by-category/', get_products_by_category, name='get_products_by_category'),

    
    # ========== SERVICE MANAGEMENT ==========
    path('services/',  service_list, name='service_list'),
    path('services/add/',  add_service, name='add_service'),
    path('services/edit/<int:id>/',  edit_service, name='edit_service'),
    path('services/delete/<int:id>/',  delete_service, name='delete_service'),
    path('services/toggle-active/<int:id>/',  toggle_service_active, name='toggle_service_active'),
    path('services/toggle-display/<int:id>/',  toggle_service_display, name='toggle_service_display'),
    
    # Service-Employee Assignment
    path('services/<int:service_id>/assign/',  assign_service_to_employee, name='assign_service_to_employee'),
    path('services/<int:service_id>/manage-employees/',  manage_service_employees, name='manage_service_employees'),
    path('service-employee/<int:service_employee_id>/remove/',  remove_employee_from_service, name='remove_employee_from_service'),
    path('service-employee/<int:service_employee_id>/toggle-availability/',  toggle_service_employee_availability, name='toggle_service_employee_availability'),

    path('employee/my-services/', my_services, name='my_services'),

    
    # ========== CUSTOMER MANAGEMENT ==========
    path('customers/',  customer_list, name='customer_list'),
    path('customers/add/',  add_customer, name='add_customer'),
    path('customers/view/<int:id>/',  view_customer, name='view_customer'),
    path('customers/edit/<int:id>/',  edit_customer, name='edit_customer'),
    path('customers/delete/<int:id>/',  delete_customer, name='delete_customer'),
    path('customers/toggle-active/<int:id>/',  toggle_customer_active, name='toggle_customer_active'),
    
    # ========== APPOINTMENT MANAGEMENT ==========
    path('appointments/',  appointment_list, name='appointment_list'),
    path('appointments/create/',  create_appointment, name='create_appointment'),
    path('appointments/create/<int:customer_id>/',  create_appointment, name='create_appointment'),
    path('appointments/view/<int:id>/',  view_appointment, name='view_appointment'),
    path('appointments/edit/<int:id>/',  edit_appointment, name='edit_appointment'),
    path('appointments/<int:appointment_id>/add-service/',  add_additional_service, name='add_additional_service'),
    path('appointments/cancel/<int:id>/',  cancel_appointment, name='cancel_appointment'),
    path('appointments/update-status/<int:id>/',  update_appointment_status, name='update_appointment_status'),
    path('appointment-service/<int:service_id>/update-status/',  update_service_status, name='update_service_status'),

    path('appointment-service/<int:service_id>/record-products/', record_product_usage, name='record_product_usage'),
    path('appointment-service/<int:service_id>/view-products/', view_product_usage, name='view_product_usage'),
    path('ajax/get-services-by-category/', get_services_by_category, name='get_services_by_category'),
    
    # ========== BILLING ==========
    path('bills/',  bill_list, name='bill_list'),
    path('bills/generate/<int:appointment_id>/',  generate_bill, name='generate_bill'),
    path('bills/view/<int:id>/',  view_bill, name='view_bill'),
    path('bills/<int:bill_id>/update-payment/',  update_payment, name='update_payment'),
    path('bills/delete/<int:id>/',  delete_bill, name='delete_bill'),
    path('bills/print/<int:id>/', print_bill, name='print_bill'),   
    
     
    # ========== AJAX ENDPOINTS ==========
    path('ajax/get-employees-for-service/',  get_employees_for_service, name='get_employees_for_service'),
    path('ajax/search-customers/',  search_customers, name='search_customers'),



]