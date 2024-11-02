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
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('resources/<str:resource_type>/<int:pk>/', views.resource_detail, name='resource_detail'),
    # User views
    path('profile/', views.profile, name='profile'),
    path('user-reports/', views.user_reports, name='user_reports'),
    path('reports/add/', views.add_report, name='add_report'),
    path('notifications/', views.notifications, name='notifications'),
    # Dashboard views
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),

    path('resource_management/', views.resource_management, name='resource_management'),
    path('resource/add_book/', views.add_book, name='add_book'),
    path('resource/add_e_journal/', views.add_e_journal, name='add_e_journal'),
    path('resource/edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('resource/edit_e_journal/<int:pk>/', views.edit_e_journal, name='edit_e_journal'),
    path('resource/delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('resource/delete_e_journal/<int:pk>/', views.delete_e_journal, name='delete_e_journal'),

    path('category_management/', views.category_management, name='category_management'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),

    path('notification_management/', views.notification_management, name='notification_management'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
