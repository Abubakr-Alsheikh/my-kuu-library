from django.urls import path
from core import views

app_name = "core"
urlpatterns = [
    path('', views.home, name='home'),
    path('resources/', views.resources, name='resources'),
    path('reports/', views.reports, name='reports'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'), # User profile
]
