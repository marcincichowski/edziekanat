from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import *
from django.utils.translation import gettext as _


class Course(Model):
    name = CharField(max_length=100,
                     unique=True,
                     verbose_name=_('Nazwa'))

    department = ForeignKey(to='edziekanat_app.Department',
                            verbose_name=_('Instytut'),
                            on_delete=CASCADE,
                            related_name="departments", default=None, null=True)

    degree = IntegerField(verbose_name=_('Stopień'),
                          default=1,
                          validators=[
                              MaxValueValidator(2),
                              MinValueValidator(1)
                          ])

    mode = ForeignKey(to='edziekanat_app.Mode',
                      verbose_name=_('tryb'),
                      on_delete=CASCADE)

    def __str__(self):
        return f"{self.name} st. {self.degree}. tryb: {self.mode.name}"

    class Meta:
        db_table = "edziekanat_app_courses"
        verbose_name = "Kierunek"
        verbose_name_plural = "Kierunki"
