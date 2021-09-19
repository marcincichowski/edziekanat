from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.users.base_user import User


# wydział > instytut > katedra
# faculty > department > chair


class StructureUnit(models.Model):
    name = models.CharField(verbose_name=_('Nazwa instytutu'),
                            max_length=100,
                            unique=True)

    location = models.CharField(_('Adres'),
                                max_length=100)

    contact_user = models.ForeignKey(User,
                                     verbose_name=_('Osoba decyzyjna'),
                                     on_delete=models.PROTECT,
                                     related_name="decision_user")

    class Meta:
        abstract = True
