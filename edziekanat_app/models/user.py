from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "Student"
        EMPLOYEE = "Employee"
        SUPERVISOR = "Supervisor"
        ADMIN = "Admin"

    role = models.CharField(_("Role"), max_length=50, choices=Roles.choices, default=Roles.STUDENT)

    acc_created_date = models.DateField(auto_now_add=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(_('password'), max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.id}"
