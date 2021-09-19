from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.base_user import User


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.ADMIN)


class AdminMore(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE)

    class Meta:
        db_table = "edziekanat_app_admins"
        verbose_name = "Administrator"
        verbose_name_plural = "Administratorzy"

class Admin(User):
    base_type = User.Roles.ADMIN
    objects = AdminManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.adminmore

    def save(self):
        if not self.pk:
            self.role = User.Roles.ADMIN
        return super().save()
