from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.contrib import messages
from .models import Appointment, TimeSlot
from django.contrib.auth import get_user_model
from django.db.models import Count
from doctors.models import Doctor
from patients.models import Patient
from datetime import date


=======
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import Appointment, TimeSlot, MedicalReport, Prescription
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from doctors.models import Doctor
from patients.models import Patient
from datetime import date
from django.core.paginator import Paginator

def get_user_role(user):
    """Robustly determine user role even if the role field is empty."""
    if not user or not user.is_authenticated:
        return ''
    
    role = user.role.upper() if user.role else ''
    
    if not role:
        if hasattr(user, 'doctor'):
            return 'DOCTOR'
        elif hasattr(user, 'patient'):
            return 'PATIENT'
        elif user.is_staff or user.is_superuser:
            return 'ADMIN'
    return role
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc


@login_required
def book_appointment(request):
<<<<<<< HEAD

    doctors = Doctor.objects.all()
    slots = TimeSlot.objects.filter(is_booked=False)

    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        slot_id = request.POST.get("slot")
        reason = request.POST.get("reason")

        print("Doctor ID from form:", doctor_id)
=======
    from django.db.models import Count
    doctors = Doctor.objects.all()
    slots = TimeSlot.objects.filter(is_booked=False).annotate(
        booking_count=Count('appointments')
    )
    
    patient_profile = getattr(request.user, 'patient', None)

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        slot_id = request.POST.get("slot")
        reason = request.POST.get("reason")
        health_issue = request.POST.get("health_issue")
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        slot = get_object_or_404(TimeSlot, id=slot_id)

        try:
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=slot.date,
                slot=slot,
<<<<<<< HEAD
                reason=reason
            )

            slot.is_booked = True
            slot.save()


            messages.success(request, "Appointment booked successfully!")
            return redirect("book_appointment")
=======
                reason=reason,
                health_issue=health_issue,
                token_number=None  # Token assigned upon approval
            )

            messages.success(request, f"Appointment request submitted successfully! Your appointment is pending approval. You will receive a token number once approved.")
            return redirect("my_appointments")
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc

        except Exception as e:
            messages.error(request, str(e))

    context = {
        "doctors": doctors,
<<<<<<< HEAD
        "slots": TimeSlot.objects.filter(is_booked=False)
=======
        "slots": slots,
        "patient": request.user,
        "profile": patient_profile
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
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
<<<<<<< HEAD
    if request.user.role != "DOCTOR":
        return redirect("login")
=======
    if get_user_role(request.user) != "DOCTOR":
        return redirect("redirect_dashboard")
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
    
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

<<<<<<< HEAD
    # if request.user.role != "PATIENT":
=======
    # if get_user_role(request.user) != "PATIENT":
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
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
<<<<<<< HEAD
    }

    return render(request, "appointments/patient_dashboard.html", {
        "upcoming": upcoming_appointments,
        "past": past_appointments,
    } , context)
=======
        "upcoming": upcoming_appointments,
        "past": past_appointments,
    }

    return render(request, "appointments/patient_dashboard.html", context)
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
    

@login_required
def redirect_dashboard(request):
    
<<<<<<< HEAD
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
=======
    user_role = get_user_role(request.user)
    
    if user_role == 'DOCTOR':
        return redirect('doctor_dashboard')
    elif user_role == 'PATIENT':
        return redirect('patient_dashboard')
    elif user_role == 'ADMIN':
        return redirect('/admin/')
    else:
        return redirect('patient_dashboard')
    
@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Generate Token Number: count of APPROVED appointments for this doctor on this day + 1
    today_approved_count = Appointment.objects.filter(
        doctor=appointment.doctor,
        appointment_date=appointment.appointment_date,
        status='APPROVED'
    ).count()
    
    appointment.token_number = today_approved_count + 1
    appointment.status = 'APPROVED'
    appointment.save()
    
    messages.success(request, f"Appointment for {appointment.patient.username} has been approved. Token No: {appointment.token_number}")
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
    return redirect('doctor_dashboard')


@login_required
def reject_appointment(request, appointment_id):
<<<<<<< HEAD
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'REJECTED'
    appointment.save()
    return redirect('doctor_dashboard')
=======
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'REJECTED'
    appointment.save()
    messages.warning(request, f"Appointment for {appointment.patient.username} has been rejected.")
    return redirect('doctor_dashboard')


def user_logout(request):
    auth_logout(request)
    return redirect('/accounts/login/')

@login_required
def doctor_appointments(request):
    if get_user_role(request.user) != "DOCTOR":
        return redirect("redirect_dashboard")
    
    doctor = Doctor.objects.get(user=request.user)
    query = request.GET.get('search', '')
    
    appointments_list = Appointment.objects.filter(
        doctor=doctor,
        status="PENDING"
    ).filter(
        Q(patient__username__icontains=query) |
        Q(reason__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10) # 10 per page
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/doctor_appointments.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def doctor_approved_appointments(request):
    if get_user_role(request.user) != "DOCTOR":
        return redirect("redirect_dashboard")
    
    doctor = Doctor.objects.get(user=request.user)
    query = request.GET.get('search', '')
    
    appointments_list = Appointment.objects.filter(
        doctor=doctor,
        status="APPROVED"
    ).filter(
        Q(patient__username__icontains=query) |
        Q(reason__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/doctor_approved.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def doctor_rejected_appointments(request):
    if get_user_role(request.user) != "DOCTOR":
        return redirect("redirect_dashboard")
    
    doctor = Doctor.objects.get(user=request.user)
    query = request.GET.get('search', '')
    
    appointments_list = Appointment.objects.filter(
        doctor=doctor,
        status="REJECTED"
    ).filter(
        Q(patient__username__icontains=query) |
        Q(reason__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/doctor_rejected.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def bulk_delete_appointments(request):
    if request.method == "POST":
        appointment_ids = request.POST.getlist('appointment_ids')
        if appointment_ids:
            if get_user_role(request.user) == "DOCTOR":
                doctor = Doctor.objects.get(user=request.user)
                deleted_count, _ = Appointment.objects.filter(id__in=appointment_ids, doctor=doctor).delete()
            else:
                deleted_count, _ = Appointment.objects.filter(id__in=appointment_ids, patient=request.user).delete()
            
            messages.success(request, f"Successfully deleted {deleted_count} appointments.")
        else:
            messages.warning(request, "No appointments selected for deletion.")
            
    return redirect(request.META.get('HTTP_REFERER', 'redirect_dashboard'))

@login_required
def patient_pending(request):
    query = request.GET.get('search', '')
    appointments_list = Appointment.objects.filter(
        patient=request.user,
        status="PENDING"
    ).filter(
        Q(doctor__user__username__icontains=query) |
        Q(reason__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/patient_pending.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def patient_approved(request):
    query = request.GET.get('search', '')
    appointments_list = Appointment.objects.filter(
        patient=request.user,
        status="APPROVED"
    ).filter(
        Q(doctor__user__username__icontains=query) |
        Q(reason__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/patient_approved.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def patient_rejected(request):
    query = request.GET.get('search', '')
    appointments_list = Appointment.objects.filter(
        patient=request.user,
        status="REJECTED"
    ).filter(
        Q(doctor__user__username__icontains=query) |
        Q(reason__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/patient_rejected.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def view_medical_report(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Ensure only the owner (patient) can view their report
    if appointment.patient != request.user:
        messages.error(request, "You do not have permission to view this report.")
        return redirect("redirect_dashboard")
        
    report = get_object_or_404(MedicalReport, appointment=appointment)
    prescriptions = report.prescriptions.all()
    
    return render(request, "appointments/view_report.html", {
        "appointment": appointment,
        "report": report,
        "prescriptions": prescriptions,
    })

@login_required
def patient_medical_reports(request):
    query = request.GET.get('search', '')
    reports_list = MedicalReport.objects.filter(
        appointment__patient=request.user
    ).filter(
        Q(appointment__doctor__user__username__icontains=query) |
        Q(health_conditions__icontains=query)
    ).order_by('-appointment__appointment_date')

    paginator = Paginator(reports_list, 10)
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)

    return render(request, "appointments/patient_reports_list.html", {
        "reports": reports,
        "query": query
    })

@login_required
def patient_health_conditions(request):
    reports = MedicalReport.objects.filter(
        appointment__patient=request.user
    ).exclude(
        health_conditions__exact=''
    ).order_by('-appointment__appointment_date')

    return render(request, "appointments/patient_health_conditions.html", {
        "reports": reports
    })

@login_required
def patient_my_doctors(request):
    # Get unique doctors from approved or completed appointments
    doctor_ids = Appointment.objects.filter(
        patient=request.user,
        status__in=['APPROVED', 'COMPLETED']
    ).values_list('doctor_id', flat=True).distinct()
    
    my_doctors = Doctor.objects.filter(id__in=doctor_ids)

    return render(request, "appointments/patient_my_doctors.html", {
        "doctors": my_doctors
    })

@login_required
def doctor_reports(request):
    if get_user_role(request.user) != "DOCTOR":
        return redirect("redirect_dashboard")
    
    doctor = Doctor.objects.get(user=request.user)
    query = request.GET.get('search', '')
    
    appointments_list = Appointment.objects.filter(
        doctor=doctor,
        status="APPROVED"
    ).filter(
        Q(patient__username__icontains=query)
    ).order_by('-appointment_date')

    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, "appointments/doctor_reports.html", {
        "appointments": appointments,
        "query": query
    })

@login_required
def edit_prescription_report(request, appointment_id):
    if get_user_role(request.user) != "DOCTOR":
        return redirect("redirect_dashboard")
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    report, created = MedicalReport.objects.get_or_create(appointment=appointment)

    if request.method == "POST":
        # Save Report fields
        report.health_conditions = request.POST.get('health_conditions')
        report.medical_details = request.POST.get('medical_details')
        report.save()

        # Handle Prescriptions (Tablets)
        # Clear old prescriptions and add new ones (simple approach for dynamic rows)
        from django.db import transaction
        with transaction.atomic():
            Prescription.objects.filter(report=report).delete()
            
            tablet_names = request.POST.getlist('tablet_name[]')
            timings = request.POST.getlist('timing[]')
            
            # Since checkboxes only send values if checked, we need to handle them carefully.
            # A common way is to use indices or prefix keys. 
            # Here I'll use a simpler approach: get the counts and look for keys like morning_0, morning_1 etc.
            
            for i in range(len(tablet_names)):
                if tablet_names[i]:
                    Prescription.objects.create(
                        report=report,
                        tablet_name=tablet_names[i],
                        timing=timings[i],
                        morning=request.POST.get(f'morning_{i}') == 'on',
                        afternoon=request.POST.get(f'afternoon_{i}') == 'on',
                        night=request.POST.get(f'night_{i}') == 'on',
                    )
        
        messages.success(request, "Report and Prescription updated successfully!")
        return redirect('doctor_reports')

    context = {
        'appointment': appointment,
        'report': report,
        'prescriptions': Prescription.objects.filter(report=report),
    }
    return render(request, 'appointments/edit_report.html', context)
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
