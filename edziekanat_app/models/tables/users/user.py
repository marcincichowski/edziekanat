from django.contrib.auth.models import AbstractUser
from django.db.models import *
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.user_manager import UserManager


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    objects = UserManager()
    role = ForeignKey(to='edziekanat_app.Role',
                      verbose_name=_('Rola'),
                      on_delete=CASCADE)

    phone = CharField(verbose_name=_('Numer kontaktowy'),
                      max_length=9,
                      default="Brak danych o numerze")

    address = CharField(verbose_name=_('Adres zamieszkania'),
                        max_length=100, default="Brak danych")
    acc_created_date = DateField(auto_now_add=True,
                                 editable=False)

    email = EmailField(_('Adres e-mail'),
                       unique=True)

    password = CharField(_('Hasło'),
                         max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "edziekanat_app_users"
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
