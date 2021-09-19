from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

import edziekanat_app.models.tables.invoice_category
from edziekanat_app.models.entities.user_manager import UserManager


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "Student"
        EMPLOYEE = "Employee"
        SUPERVISOR = "Supervisor"
        ADMIN = "Admin"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    role = models.CharField(_("Rola"),
                            max_length=50,
                            choices=Roles.choices,
                            default=Roles.STUDENT)

    acc_created_date = models.DateField(auto_now_add=True,
                                        editable=False)

    email = models.EmailField(_('Adres e-mail'),
                              unique=True)

    password = models.CharField(_('Hasło'),
                                max_length=128)

    username = None



    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    objects = UserManager()

    class Meta:
        db_table = "edziekanat_app_users"
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"






