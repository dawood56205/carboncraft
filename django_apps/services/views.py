from django.shortcuts import render , get_object_or_404, redirect
from services.models import *
# Create your views here.
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service.html', {'services': services})



def book_service(request, service_id):
    # 1. Get the service the user wants to buy
    service = get_object_or_404(Service, pk=service_id)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        address = request.POST.get('address') # Added this since it's in your model
        notes = request.POST.get('notes')

        # Basic validation
        if not first_name or not email:
            return render(request, 'bookingform.html', {
                'service': service,
                'error': 'First name and email are required'
            })

        # 2. Create the booking and CAPTURE the new object in a variable
        new_booking = ServiceBooking.objects.create(
            service=service,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            booking_date=booking_date,
            booking_time=booking_time,
            address=address,
            notes=notes
        )

        # 3. Pass the NEWLY CREATED booking to the success page
        return render(request, 'servicesuccess.html', {'booking': new_booking})

    # If GET, just show the empty form
    return render(request, 'bookingform.html', {'service': service})

