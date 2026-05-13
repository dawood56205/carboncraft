from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from carboncraftstudio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("",views.home, name="home"),
    path("about/",views.about, name="about"),
    path("__reload__/", include("django_browser_reload.urls")),
    path('products/', include('products.urls')),
    path('services/', include('services.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('API.urls')),
    path('adminstudio/', include('dashboard.urls')),
    path('ai/', include('AI_AGENTS.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
