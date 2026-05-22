from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from services import views
urlpatterns = [
    
    
  path('', views.service_list, name = 'services'),
  path('book/<int:service_id>', views.book_service, name = 'booking'),
  
 
]