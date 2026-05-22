from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from AI_AGENTS import views
urlpatterns = [

  path('', views.Ai_agents, name='ai_agents'),
  path('consultant/', views.ai_consultant_view, name='ai_consultant'),  
  path('car_navigator/', views.ai_consultant_view2, name='car_navigator'),  
  path('car_specs/', views.car_specs_view, name='car_specs'),
  path('engine_recommend/', views.engine_recommendation_view, name='engine_recommend'),
  path('compare/', views.car_comparison_view, name='ai_compare'),
  path("diagnose/", views.diagnose, name="diagnose"),
]