from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.employee import Employee


class Subject(models.Model):
    def user_validator(user_id):
        user = Employee.objects.filter(id=user_id).first()
        if user.job.name not in ["Wykładowca"]:
            raise ValidationError(u'Użytkownik musi być pracownikiem dziekanatu!')

    department = models.ForeignKey('edziekanat_app.Department',
                                   verbose_name=_('Instytut'),
                                   on_delete=models.CASCADE)

    teacher = models.ForeignKey('edziekanat_app.Employee',
                                verbose_name=_('Prowadzący'),
                                on_delete=models.PROTECT,
                                validators=[user_validator])

    name = models.CharField(max_length=70)
    ects = models.IntegerField()
    sem = models.IntegerField()

    def __str__(self):
        return f"{self.name} semestr: {self.sem}."

    class Meta:
        db_table = "edziekanat_app_subjects"
        unique_together = ['department', 'name']
        verbose_name = "Przedmiot"
        verbose_name_plural = "Przedmioty"
