from django.urls import path
from .views import available_slots
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("book/", views.book_appointment, name="book_appointment"),
    path('slots/<int:doctor_id>/', available_slots, name='available_slots'),
    path("my/", views.my_appointments, name="my_appointments"),
    path('redirect-dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path("doctor-dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path("patient-dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),

]
