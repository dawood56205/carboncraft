from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from products import views
urlpatterns = [
    
    
  path("", views.product_list, name = "productlist"),
  path('<int:pro_id>/', views.pro_det, name="pro_det"),
  path('order/', include('orders.urls') ),

]