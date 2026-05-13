from django.shortcuts import render
from products.models import products

def home(request):
  latest_products = products.objects.all().order_by('-date_added')[:4]
  return render (request, 'home.html', {'latest_products': latest_products})

def about(request):
  return render (request, 'about.html')