from django.db import models
from django.utils.translation import gettext as _


class Role(models.Model):
    name = models.CharField(_('Rola'),
                            max_length=70,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "edziekanat_app_roles"
        verbose_name = "Rola"
        verbose_name_plural = "Role"
