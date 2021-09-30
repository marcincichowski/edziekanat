from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.employee import Employee


class Subject(models.Model):
    TYPES = (
        ('Projekt', 'Projekt'),
        ('Wykład', 'Wykład'),
        ('Ćwiczenia', 'Ćwiczenia'),
        ('Laboratorium', 'Laboratorium')
    )
    type = models.CharField(max_length=50, choices=TYPES, default=None, null=True)

    def user_validator(user_id):
        user = Employee.objects.filter(id=user_id).first()
        if user.job.name not in ["Wykładowca", "Dyrektor instytutu"]:
            raise ValidationError(u'Użytkownik musi być wykładowcą!')

    course = models.ForeignKey('edziekanat_app.Course',
                                   verbose_name=_('Kierunek'),
                                   on_delete=models.CASCADE, default=None, null=True)



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
        verbose_name = "Przedmiot"
        verbose_name_plural = "Przedmioty"
