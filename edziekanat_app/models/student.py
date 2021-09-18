from edziekanat_app.models.user import User
from django.db import models


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.STUDENT)


class StudentMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.STUDENT
        return super().save()
