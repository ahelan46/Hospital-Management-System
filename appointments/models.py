from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from doctors.models import Doctor


User = settings.AUTH_USER_MODEL


    
class DoctorAvailability(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='availability'
    )

    DAY_CHOICES = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )

    day = models.CharField(max_length=3, choices=DAY_CHOICES)

    start_time = models.TimeField()
    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_available:

            today = date.today()

            weekday_map = {
                0: 'MON',
                1: 'TUE',
                2: 'WED',
                3: 'THU',
                4: 'FRI',
                5: 'SAT',
                6: 'SUN',
            }


            for i in range(30):  # generate slots for next 30 days
                future_date = today + timedelta(days=i)

                # match weekday
                # if future_date.strftime('%a').upper().startswith(self.day.strftime('%a').upper()):
                if weekday_map[future_date.weekday()] == self.day:

                    create_time_slots(
                        doctor=self.doctor,
                        date=future_date,
                        start_time=self.start_time,
                        end_time=self.end_time,
                        duration=30
                    )

    def __str__(self):
        return f"{self.doctor} - {self.day}"



class TimeSlot(models.Model):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=1)
    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'start_time'],
                name='unique_slot'
            )
        ]

    def __str__(self):
        return f"{self.doctor} | {self.date} | {self.start_time}-{self.end_time}"

def create_time_slots(doctor, date, start_time, end_time, duration):

    start = datetime.combine(date, start_time)
    end = datetime.combine(date, end_time)
    
    while start < end:
        slot_end = start + timedelta(minutes=duration)

        TimeSlot.objects.get_or_create(
            doctor=doctor,
            date=date,
            start_time=start.time(),
            defaults={
                "end_time": slot_end.time(),
                "is_booked": False,
                "capacity": doctor.max_patients_per_slot
            }
        )

        start = slot_end

    
class Appointment(models.Model):

    STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )

    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateField()
    slot = models.ForeignKey(
        'appointments.TimeSlot',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
   
    reason = models.TextField()
    health_issue = models.CharField(max_length=255, blank=True, null=True)
    token_number = models.PositiveIntegerField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.patient == self.doctor:
            raise ValidationError("Doctor and patient cannot be the same.")

        if self.slot and self.slot.doctor != self.doctor:
            raise ValidationError("Selected slot does not belong to this doctor.")

        if self.slot and self.slot.date != self.appointment_date:
            raise ValidationError("Appointment date does not match slot date.")

    def save(self, *args, **kwargs):
        from django.db import transaction

        with transaction.atomic():
            if not self.pk: # New appointment
                current_bookings = self.slot.appointments.count()
                if current_bookings >= self.slot.capacity:
                    raise ValidationError("This slot has already reached its maximum capacity!")

                self.full_clean()
                super().save(*args, **kwargs)

                # Update is_booked if capacity is now full
                if self.slot.appointments.count() >= self.slot.capacity:
                    self.slot.is_booked = True
                    self.slot.save(update_fields=['is_booked'])
            else:
                super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        slot = self.slot
        super().delete(*args, **kwargs)

        # Check if slot should be marked as available again
        if slot.appointments.count() < slot.capacity:
            slot.is_booked = False
            slot.save(update_fields=['is_booked'])
        
    def __str__(self):
        return f"{self.patient} → {self.doctor} ({self.appointment_date})"
    
    def appointment_time(self):
        return f"{self.slot.date} | {self.slot.start_time}"

class MedicalReport(models.Model):
    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name='medical_report'
    )
    health_conditions = models.TextField(blank=True, null=True)
    medical_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report for {self.appointment.patient.username} - {self.appointment.appointment_date}"

class Prescription(models.Model):
    TIMING_CHOICES = (
        ('Before Eating', 'Before Eating'),
        ('After Eating', 'After Eating'),
    )

    report = models.ForeignKey(
        MedicalReport,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    tablet_name = models.CharField(max_length=255)
    timing = models.CharField(max_length=20, choices=TIMING_CHOICES)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    night = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tablet_name} for report {self.report.id}"



    


   

    