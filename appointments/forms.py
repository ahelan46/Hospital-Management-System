from django import forms
from .models import Appointment, TimeSlot

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'slot', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # show only unbooked slots
        self.fields['slot'].queryset = TimeSlot.objects.filter(is_booked=False)
