from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.university_structure.structure_unit import StructureUnit
from django.core.exceptions import ValidationError

from edziekanat_app.models.tables.users.employee import Employee


def user_validator(user_id):
    user = Employee.objects.filter(user_id=user_id).first()
    if user.job.name not in ["Pracownik dziekanatu", "Dyrektor instytutu"]:
        raise ValidationError(u'Użytkownik musi być pracownikiem dziekanatu!')


class Department(StructureUnit):
    head = models.ForeignKey('edziekanat_app.Employee',
                             verbose_name=_('Dyrektor instytutu'),
                             on_delete=models.PROTECT,
                             validators=[user_validator])

    contact_user = models.ForeignKey('edziekanat_app.Employee',
                                     verbose_name=_('Osoba decyzyjna'),
                                     on_delete=models.PROTECT,
                                     related_name="department_decision_user",
                                     validators=[user_validator])

    def __str__(self):
        return f"{self.name} {self.location}"

    class Meta:
        db_table = "edziekanat_app_departments"
        verbose_name = "Instytut"
        verbose_name_plural = "Instytuty"
