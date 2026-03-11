from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=120)

    experience_years = models.PositiveIntegerField()

    license_number = models.CharField(max_length=50, unique=True)

    phone = models.CharField(max_length=15)

    is_available = models.BooleanField(default=True)
<<<<<<< HEAD
=======
    max_patients_per_slot = models.PositiveIntegerField(default=1)
>>>>>>> 3475266f108007b774f3a8cd5bbf15ec29df5ffc

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
