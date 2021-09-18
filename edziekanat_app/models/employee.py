from django.db import models
from edziekanat_app.models.user import User


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.EMPLOYEE)


class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.EMPLOYEE
        return super().save()
