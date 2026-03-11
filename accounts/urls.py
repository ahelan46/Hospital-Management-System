from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.patient_signup, name='patient_signup'),
]
