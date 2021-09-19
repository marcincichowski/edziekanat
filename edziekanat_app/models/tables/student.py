from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.user import User
from edziekanat_app.models.tables.course import Course


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.STUDENT)


class StudentMore(models.Model):
    user = models.OneToOneField(User,
                                verbose_name=_('Użytkownik'),
                                on_delete=models.CASCADE)

    index = models.CharField(max_length=6, unique=True)

    sem = models.IntegerField(verbose_name=_('Semestr'),
                              default=1)
    year = models.IntegerField(verbose_name=_('Rok'),
                               default=1)
    degree = models.IntegerField(verbose_name=_('Stopień'),
                                 default=1)

    course = models.ForeignKey(Course,
                               verbose_name=_('Kierunek'),
                               blank=False,
                               on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.order_id = f'{self.user.id:06}'
        super(StudentMore, self).save(*args, **kwargs)

    class Meta:
        db_table = "edziekanat_app_students"


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "Student"
        verbose_name_plural = "Studenci"

    def save(self):
        if not self.pk:
            self.role = User.Roles.STUDENT
        return super().save()
