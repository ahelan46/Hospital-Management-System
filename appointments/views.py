from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, TimeSlot
from django.contrib.auth import get_user_model
from django.db.models import Count
from doctors.models import Doctor
from patients.models import Patient
from datetime import date




@login_required
def book_appointment(request):

    doctors = Doctor.objects.all()
    slots = TimeSlot.objects.filter(is_booked=False)

    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        slot_id = request.POST.get("slot")
        reason = request.POST.get("reason")

        print("Doctor ID from form:", doctor_id)
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        slot = get_object_or_404(TimeSlot, id=slot_id)

        try:
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=slot.date,
                slot=slot,
                reason=reason
            )

            slot.is_booked = True
            slot.save()


            messages.success(request, "Appointment booked successfully!")
            return redirect("book_appointment")

        except Exception as e:
            messages.error(request, str(e))

    context = {
        "doctors": doctors,
        "slots": TimeSlot.objects.filter(is_booked=False)
    }

    return render(request, "appointments/book.html", context)

def available_slots(request, doctor_id):

    slots = TimeSlot.objects.filter(
        doctor_id=doctor_id,
        
        is_booked=False
    ).order_by('start_time')

    return render(request, 'appointments/slots.html', {
        'slots': slots
    })

def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-appointment_date')

    return render(request, "appointments/my_appointments.html", {
        "appointments": appointments
    })

@login_required
def doctor_dashboard(request):
    if request.user.role != "DOCTOR":
        return redirect("login")
    
    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('-appointment_date')

    total = appointments.count()
    approved = appointments.filter(status="APPROVED").count()
    pending = appointments.filter(status="PENDING").count()
    rejected = appointments.filter(status="REJECTED").count()

    context = {
        "appointments": appointments,
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
    }

    return render(request, "appointments/doctor_dashboard.html", context)

@login_required
def patient_dashboard(request):

    # if request.user.role != "PATIENT":
    #     return redirect("redirect_dashboard")

    upcoming_appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_date__gte=date.today()
    ).order_by("appointment_date")

    past_appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_date__lt=date.today()
    ).order_by("-appointment_date")


    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')

    total = appointments.count()
    approved = appointments.filter(status="APPROVED").count()
    pending = appointments.filter(status="PENDING").count()
    rejected = appointments.filter(status="REJECTED").count()

    context = {
        "appointments": appointments,
        "total": total,
        "approved": approved,
        "pending": pending,
        "rejected": rejected,
    }

    return render(request, "appointments/patient_dashboard.html", {
        "upcoming": upcoming_appointments,
        "past": past_appointments,
    } , context)
    

@login_required
def redirect_dashboard(request):
    
    if request.user.role == 'DOCTOR':
        return redirect('doctor_dashboard')
    elif request.user.role == 'PATIENT':
        return redirect('patient_dashboard')
    elif request.user.role == 'ADMIN':
        return redirect('/admin/')
    else:
        return redirect('book_appointment')
    
@login_required
def approve_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'APPROVED'
    appointment.save()
    return redirect('doctor_dashboard')


@login_required
def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'REJECTED'
    appointment.save()
    return redirect('doctor_dashboard')