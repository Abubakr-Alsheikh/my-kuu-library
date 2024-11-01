from django.urls import path
from core import views
from my_kuu_library import settings
from django.conf.urls.static import static

app_name = "core"
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('resources/', views.resources, name='resources'),
    path('reports/', views.reports, name='reports'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('resources/<str:resource_type>/<int:pk>/', views.resource_detail, name='resource_detail'), # Updated path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
