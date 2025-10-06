from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    birth_date = models.DateField(null=True, blank=True)