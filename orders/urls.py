from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from orders import views
urlpatterns = [
    
    
  path('<int:pro_id>', views.checkout_view, name="checkout"),

  path("services", views.services, name="services"),
  path('history/', views.order_history, name='order_history'),
]