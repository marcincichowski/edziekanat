from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.university_structure.department import Department


class Subject(models.Model):
    department = models.ForeignKey(Department,
                                   verbose_name=_('Instytut'),
                                   on_delete=models.CASCADE)

    name = models.CharField(max_length=70)
    ects = models.IntegerField()
    sem = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "edziekanat_app_subjects"
        unique_together = ['department', 'name']
        verbose_name = "Przedmiot"
        verbose_name_plural = "Przedmioty"
