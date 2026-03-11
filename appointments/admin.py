from django.contrib import admin
from .models import Appointment
from .models import Appointment, DoctorAvailability, TimeSlot, create_time_slots
from django.core.exceptions import ValidationError

from datetime import time
from django import forms
from accounts.models import User
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    
    list_display = (
        'patient',
        'doctor',
        'appointment_date',
        
        'status'
    )

    
    list_filter = ('status', 'appointment_date')


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):

    list_display = ('doctor', 'day', 'start_time', 'end_time', 'is_available')
    list_filter = ('day', 'is_available')

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be greater than start time.")

@admin.action(description="Generate Slots (9AM–5PM)")
def generate_slots(modeladmin, request, queryset):
    for doctor_slot in queryset:
        create_time_slots(
            doctor=doctor_slot.doctor,
            date=doctor_slot.date,
            start_time=time(9, 0),
            end_time=time(17, 0),
            duration=30
        )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):

    list_display = ('doctor', 'date', 'start_time', 'is_booked')
    list_filter = ('is_booked', 'date')
    actions = [generate_slots]


# admin.site.register(TimeSlot, TimeSlotAdmin)

class AppointmentAdminForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only Doctors
        self.fields['doctor'].queryset = \
            self.fields['doctor'].queryset.filter(user__role='DOCTOR')

        # Only Patients
        self.fields['patient'].queryset = \
            self.fields['patient'].queryset.filter(user__role='PATIENT')