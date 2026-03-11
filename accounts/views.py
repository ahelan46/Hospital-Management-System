<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User
from patients.models import Patient
import datetime

def patient_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Patient specific fields
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        blood_group = request.POST.get('blood_group')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'registration/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'registration/signup.html')

        try:
            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='PATIENT'
            )
            
            # Create Patient Profile
            Patient.objects.create(
                user=user,
                date_of_birth=dob,
                blood_group=blood_group,
                gender=gender,
                phone=phone,
                address=address
            )

            login(request, user)
            messages.success(request, f"Welcome {username}! Your account has been created.")
            return redirect('redirect_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'registration/signup.html')

    return render(request, 'registration/signup.html', {
        'blood_groups': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'genders': ['MALE', 'FEMALE', 'OTHER']
    })
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
