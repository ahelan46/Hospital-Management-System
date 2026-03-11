from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Patient(models.Model):
<<<<<<< HEAD

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField()

    blood_group = models.CharField(max_length=5)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    emergency_contact = models.CharField(max_length=15)

=======
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
