from django.db.models import *
from django.utils.translation import gettext as _


class Mode(Model):
    name = CharField(max_length=30,
                            unique=True,
                            verbose_name=_('Nazwa'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "edziekanat_app_study_modes"
        verbose_name = "Tryb"
        verbose_name_plural = "Tryby"
