from django.db import models
from edziekanat_app.models.user import User


class SupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.SUPERVISOR)


class Supervisor(User):
    objects = SupervisorManager()

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.SUPERVISOR
        return super().save()
