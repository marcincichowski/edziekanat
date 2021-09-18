from edziekanat_app.models.user import User
from django.db import models


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.ADMIN)


class Admin(User):
    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.ADMIN
        return super().save()