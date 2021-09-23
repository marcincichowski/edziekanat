from django.db.models import *
from django.utils.translation import gettext as _


class Employee(Model):
    base_role = 'Pracownik'

    job = ForeignKey(to='edziekanat_app.Job',
                     verbose_name=_('Stanowisko'),
                     on_delete=CASCADE, default=None, null=True)

    boss = OneToOneField(to='edziekanat_app.User',
                         verbose_name=_('Przełożony'),
                         on_delete=CASCADE,
                         related_name="bosses", default=None, null=True)

    user = OneToOneField(to='edziekanat_app.User',
                         verbose_name=_('Użytkownik'),
                         on_delete=CASCADE)

    def __str__(self):
        return f"{self.user.__str__()} (stanowisko: {self.job.__str__()})"

    class Meta:
        db_table = "edziekanat_app_employees"
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"
