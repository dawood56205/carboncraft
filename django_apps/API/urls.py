from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.get_data),
  path('add/', views.add_items, name='add_items')
]