from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.custom_login, name='login'),
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
    path('form/<str:unique_id>/', views.attendee_form, name='attendee_form'),
    #path('form/<str:unique_id>/', attendee_admin_site.urls, name='attendee_form'),
    path('check_in/<str:unique_id>/', views.check_in, name='check_in'),
    path('watchman/dashboard/<str:unique_id>', views.watchman_dashboard, name='watchman_dashboard'),
    path('form_success/', views.form_success, name='form_success'),
    path('arrival_success/', views.arrival_success, name='arrival_success'),
    path('already_arrived/', views.already_arrived, name='already_arrived'),
    path('already_submitted/', views.already_submitted, name='already_submitted'),
    path('register/', views.register, name='register'),
    path('scan_qr_code/', views.scan_qr_code, name='scan_qr_code'),
    path('scan_attendee/<str:unique_id>/', views.scan_attendee, name='scan_attendee'),
    path('stall_dashboard/', views.stall_dashboard, name='stall_dashboard'),
]
