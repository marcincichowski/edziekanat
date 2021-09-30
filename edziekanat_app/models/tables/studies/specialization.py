from django.db import models
from django.utils.translation import gettext as _


class Specialization(models.Model):
    course = models.ForeignKey(to='edziekanat_app.Course',
                               verbose_name=_('Kierunek'),
                               on_delete=models.CASCADE,
                               default=None, null=True)

    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=_('Nazwa'))

    def __str__(self):
        return f"{self.name} (kierunek: {self.course.__str__()})"

    class Meta:
        db_table = "edziekanat_app_spectializations"
        verbose_name = "Specjalizacja"
        verbose_name_plural = "Specjalizacje"
