from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.user import User


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.ADMIN)


class AdminMore(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE)

    class Meta:
        db_table = "edziekanat_app_admins"


class Admin(User):
    class Meta:
        proxy = True
        verbose_name = "Administrator"
        verbose_name_plural = "Administratorzy"

    def save(self):
        if not self.pk:
            self.role = User.Roles.ADMIN
        return super().save()
