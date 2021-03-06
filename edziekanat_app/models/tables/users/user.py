import datetime

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
    birth_date = DateField(verbose_name=_('Data urodzenia'),
                           default=datetime.date.today)

    email = EmailField(_('Adres e-mail'),
                       unique=True)

    allow_email_send = BooleanField(verbose_name=_('Zgoda na korespondencje'),
                                    default=True)

    password = CharField(_('Hasło'),
                         max_length=128)

    #inbox = ForeignKey(to='edziekanat_app.Inbox',
    #                   verbose_name=_('Skrzynka pocztowa'),
    #                   on_delete=CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "edziekanat_app_users"
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
