from django.urls import path
from dashboard.views import AdminDashboardView  # etc.

from dashboard import views

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    # path("login/", views.login, name = 'login')
    path('order/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete_service'),
    path('add-service/', views.add_service, name='add_service'),
    path('booking/<int:pk>/', views.booking_detail_view, name='booking_detail'),
]