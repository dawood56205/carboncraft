from django.shortcuts import render, redirect, get_object_or_404
from .models import Order 
from products.models import products

def checkout_view(request, pro_id):
    # 1. Fetch the service (Product) being booked
    product = get_object_or_404(products, pk=pro_id)

    if request.method == "POST":
        # 2. Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        quantity = int(request.POST.get('quantity', 1))

        # 3. Save the order to the database
        order = Order.objects.create(
            product=product,
            first_name=first_name,
            last_name=last_name,
            phone = phone,
            email=email,
            address=address,
            city=city,
            quantity=quantity,
            total_price=product.price * quantity # Captures the price at time of purchase
        )
        
        # 4. Success: Send them to the thank you page
        return render(request, 'success.html', {'order': order, 'product':product})

    # 5. GET: Show the checkout form with the product details
    return render(request, 'orders.html', {'product': product})

def services(request):
    return render(request, 'services.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required  # Redirects to login page if user isn't signed in
def order_history(request):
    # CRITICAL: We filter by request.user so users cannot guess URLs 
    # and see other people's data.
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'history.html', {'orders': orders})