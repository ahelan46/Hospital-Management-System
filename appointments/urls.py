from django.urls import path
from .views import available_slots
from . import views
<<<<<<< HEAD
from django.contrib.auth.views import LogoutView
=======
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc

urlpatterns = [
    path("book/", views.book_appointment, name="book_appointment"),
    path('slots/<int:doctor_id>/', available_slots, name='available_slots'),
    path("my/", views.my_appointments, name="my_appointments"),
    path('redirect-dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path("doctor-dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
<<<<<<< HEAD
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path("patient-dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
=======
    path('patient/pending/', views.patient_pending, name='patient_pending'),
    path('patient/approved/', views.patient_approved, name='patient_approved'),
    path('patient/rejected/', views.patient_rejected, name='patient_rejected'),
    path('patient/report/<int:appointment_id>/', views.view_medical_report, name='view_medical_report'),
    path('patient/reports-list/', views.patient_medical_reports, name='patient_medical_reports'),
    path('patient/health-conditions/', views.patient_health_conditions, name='patient_health_conditions'),
    path('patient/my-doctors/', views.patient_my_doctors, name='patient_my_doctors'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/approved/', views.doctor_approved_appointments, name='doctor_approved'),
    path('doctor/rejected/', views.doctor_rejected_appointments, name='doctor_rejected'),
    path('doctor/bulk-delete/', views.bulk_delete_appointments, name='bulk_delete_appointments'),
    path('doctor/reports/', views.doctor_reports, name='doctor_reports'),
    path('doctor/reports/edit/<int:appointment_id>/', views.edit_prescription_report, name='edit_prescription_report'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('logout/', views.user_logout, name='logout'),
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc

]
