from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.university_structure.structure_unit import StructureUnit
from edziekanat_app.models.tables.users.base_user import User


class Faculty(StructureUnit):
    dean = models.ForeignKey(User,
                             verbose_name=_('Dziekan'),
                             on_delete=models.CASCADE)

    contact_user = models.ForeignKey(User,
                                     verbose_name=_('Osoba decyzyjna'),
                                     on_delete=models.PROTECT,
                                     related_name="faculty_decision_user")

    def __str__(self):
        return f"{self.name} {self.location}"

    class Meta:
        db_table = "edziekanat_app_faculties"
        verbose_name = "Wydział"
        verbose_name_plural = "Wydziały"
