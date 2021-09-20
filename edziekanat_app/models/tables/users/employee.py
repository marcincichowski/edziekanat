from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.role import Role


class Employee(models.Model):
    base_role = 'Pracownik'

    user = models.OneToOneField(to='edziekanat_app.User',
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE)

    class Meta:
        db_table = "edziekanat_app_employees"
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"
