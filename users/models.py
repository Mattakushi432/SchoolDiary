
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("STUDENT", "Student"),
        ("TEACHER", "Teacher"),
        ("ADMIN", "Admin"),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="STUDENT")
    birth_date = models.DateField(null=True, blank=True)