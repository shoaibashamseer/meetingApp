from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
    path('form/<str:unique_id>/', views.attendee_form, name='attendee_form'),
    path('check_in/<str:unique_id>/', views.check_in, name='check_in'),
    path('form_success/', views.form_success, name='form_success'),
    path('arrival_success/', views.arrival_success, name='arrival_success'),
    path('already_arrived/', views.already_arrived, name='already_arrived'),
    path('already_submitted/', views.already_submitted, name='already_submitted'),
]
