from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.role import Role


class Student(models.Model):
    base_role = 'Student'

    user = models.OneToOneField(to='edziekanat_app.User',
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE,
                                related_name="students")

    index = models.CharField(null=True, max_length=6)

    sem = models.IntegerField(verbose_name=_('Semestr'),
                              default=1)

    year = models.IntegerField(verbose_name=_('Rok'),
                               default=1)

    degree = models.IntegerField(verbose_name=_('Stopień'),
                                 default=1)

    course = models.ForeignKey(to='edziekanat_app.Course',
                               verbose_name=_('Kierunek'),
                               on_delete=models.PROTECT,
                               default=None, null=True)

    class Meta:
        db_table = "edziekanat_app_students"
        verbose_name = "Student"
        verbose_name_plural = "Studenci"


    def __str__(self):
        return f"{self.user.__str__()} {self.more.index}"
