from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Role choices for the system
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        AGENT = "AGENT", "Support Agent"
        MANAGER = "MANAGER", "Manager"

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    # Use email for login instead of username if preferred, 
    # but keeping it simple for now.
    def __str__(self):
        return f"{self.username} - {self.role}"

class StudentProfile(models.Model):
    # Linking profile to the main User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    student_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.student_id