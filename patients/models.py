from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField()

    blood_group = models.CharField(max_length=5)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    emergency_contact = models.CharField(max_length=15)

    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
