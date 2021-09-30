from django.db import models
from django.utils.translation import gettext as _


class Job(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=_('Nazwa'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "edziekanat_app_jobs"
        verbose_name = "Stanowisko"
        verbose_name_plural = "Stanowiska"
