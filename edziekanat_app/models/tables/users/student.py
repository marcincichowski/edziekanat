from django.db.models import *
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField


class Student(Model):
    base_role = 'Student'
    user = OneToOneField(to='edziekanat_app.User',
                         verbose_name=_('Użytkownik'),
                         on_delete=CASCADE,
                         related_name="students")



    index = CharField(null=True, max_length=6)

    sem = IntegerField(verbose_name=_('Semestr'),
                       default=1)

    year = IntegerField(verbose_name=_('Rok'),
                        default=1)


    course = ForeignKey(to='edziekanat_app.Course',
                        verbose_name=_('Kierunek'),
                        on_delete=PROTECT,
                        default=None, null=True)

    specialization = ForeignKey(to='edziekanat_app.Specialization',
                                verbose_name=_('Specjalizacja'),
                                on_delete=CASCADE,
                                default=None, null=True)

    class Meta:
        db_table = "edziekanat_app_students"
        verbose_name = "Student"
        verbose_name_plural = "Studenci"

    def __str__(self):
        return f"{self.user.__str__()} (nr indeksu: {self.index})"
