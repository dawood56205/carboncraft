from django.shortcuts import render, redirect
from django.views.generic import ListView
from products.models import products
from services.models import Service
from services.models import ServiceBooking
from orders.models import Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from services.models import Service




class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'admin_home.html'
    context_object_name = 'all_orders'
    ordering = ['-id']

    def test_func(self):
        return self.request.user.is_staff
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Core Collections
        all_orders = Order.objects.all()
        context['all_services'] = Service.objects.all()
        context['all_products'] = products.objects.all()
        context['all_bookings'] = ServiceBooking.objects.all().order_by('-id')
        
        # Calculated Stats
        order_revenue = sum(order.total_price for order in all_orders)
        
        service_revenue = 0
        for booking in context['all_bookings']:
            if booking.status != 'cancelled':
                try:
                    service_revenue += float(booking.service.price)
                except (ValueError, TypeError):
                    pass
        
        context['order_revenue'] = order_revenue
        context['service_revenue'] = service_revenue
        context['total_revenue'] = order_revenue + service_revenue
        
        return context
# --- 2. Add Product (Restricted to Staff) ---
@user_passes_test(lambda u: u.is_staff, login_url='home')
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product')
        p_type = request.POST.get('type')
        p_details = request.POST.get('details')
        p_warranty = request.POST.get('warranty', 'N/A')
        p_price = request.POST.get('price')
        p_photo = request.FILES.get('photo')

        new_product = products(
            user=request.user,
            product=product_name,
            type=p_type,
            details=p_details,
            warranty=p_warranty,
            price=p_price,
            photo=p_photo
        )
        new_product.save()
        return redirect('admin_dashboard')

    return render(request, 'product_form.html')




# --- Edit Product ---
@user_passes_test(lambda u: u.is_staff, login_url='home')
def edit_product(request, pk):
    product_obj = get_object_or_404(products, pk=pk)
    
    if request.method == "POST":
        # Update the fields from the POST data
        product_obj.product = request.POST.get('product')
        product_obj.type = request.POST.get('type')
        product_obj.details = request.POST.get('details')
        product_obj.warranty = request.POST.get('warranty')
        product_obj.price = request.POST.get('price')
        
        # Only update the photo if a new one is uploaded
        if request.FILES.get('photo'):
            product_obj.photo = request.FILES.get('photo')
            
        product_obj.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_product.html', {'product': product_obj})

# --- Delete Product ---
@user_passes_test(lambda u: u.is_staff, login_url='home')
def delete_product(request, pk):
    product_obj = get_object_or_404(products, pk=pk)
    product_obj.delete()
    return redirect('admin_dashboard')



# --- Edit Service ---
@user_passes_test(lambda u: u.is_staff, login_url='home')
def edit_service(request, pk):
    service_obj = get_object_or_404(Service, pk=pk)
    
    if request.method == "POST":
        service_obj.service_name = request.POST.get('name')
        service_obj.description = request.POST.get('description')
        service_obj.price = request.POST.get('price')
        
        service_obj.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_service.html', {'service': service_obj})

# --- Delete Service ---
@user_passes_test(lambda u: u.is_staff, login_url='home')
def delete_service(request, pk):
    service_obj = get_object_or_404(Service, pk=pk)
    service_obj.delete()
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_staff, login_url='home')
def order_detail_view(request, pk):
    """
    Fetches a single order for the dossier view.
    """
    order = get_object_or_404(Order, pk=pk)
    
    # Logic for status updates if a POST request is sent from the detail page
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status # Ensure you have a status field in your model
            order.save()
            return redirect('order_detail', pk=order.pk)

    return render(request, 'order_det.html', {'order': order})

@user_passes_test(lambda u: u.is_staff, login_url='home')
def add_service(request):
    if request.method == "POST":
        service_name = request.POST.get('service_name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        # Create and save the new service
        Service.objects.create(
            service_name=service_name,
            price=price,
            description=description
        )
        return redirect('admin_dashboard')

    return render(request, 'add_service.html')

@user_passes_test(lambda u: u.is_staff, login_url='home')
def booking_detail_view(request, pk):
    """
    Fetches a single service booking for the dossier/receipt view.
    """
    booking = get_object_or_404(ServiceBooking, pk=pk)
    return render(request, 'booking_det.html', {'booking': booking})