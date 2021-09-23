from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.role import Role


class Admin(models.Model):
    base_role = 'Administrator'

    user = models.OneToOneField(to='edziekanat_app.User',
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.__str__()} ({self.base_role.upper()})"

    class Meta:
        db_table = "edziekanat_app_administrators"
        verbose_name = "Administrator"
        verbose_name_plural = "Administratorzy"
