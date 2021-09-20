from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.user_manager import UserManager


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    objects = UserManager()
    role = models.ForeignKey(to='edziekanat_app.Role',
                             verbose_name=_('Rola'),
                             on_delete=models.CASCADE)

    acc_created_date = models.DateField(auto_now_add=True,
                                        editable=False)

    email = models.EmailField(_('Adres e-mail'),
                              unique=True)

    password = models.CharField(_('Hasło'),
                                max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    class Meta:
        db_table = "edziekanat_app_users"
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"
