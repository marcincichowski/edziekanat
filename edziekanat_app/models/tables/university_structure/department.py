from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.university_structure.structure_unit import StructureUnit
from edziekanat_app.models.tables.user import User


class Department(StructureUnit):
    head = models.ForeignKey(User,
                             verbose_name=_('Kierownik instytutu'),
                             on_delete=models.PROTECT)

    contact_user = models.ForeignKey(User,
                                     verbose_name=_('Osoba decyzyjna'),
                                     on_delete=models.PROTECT,
                                     related_name="department_decision_user")

    def __str__(self):
        return f"{self.name} {self.location}"

    class Meta:
        db_table = "edziekanat_app_departments"
        verbose_name = "Instytut"
        verbose_name_plural = "Instytuty"
