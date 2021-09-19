from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.user import User


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.EMPLOYEE)


class EmployeeMore(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE)

    class Meta:
        db_table = "edziekanat_app_employees"


class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"

    def save(self):
        if not self.pk:
            self.role = User.Roles.EMPLOYEE
        return super().save()
