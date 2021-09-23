from django.db import models
from django.utils.translation import gettext as _
# wydział > instytut > katedra
# faculty > department > chair


class StructureUnit(models.Model):
    name = models.CharField(verbose_name=_('Nazwa instytutu'),
                            max_length=100,
                            unique=True)

    location = models.CharField(_('Adres'),
                                max_length=100)

    contact_user = models.ForeignKey('edziekanat_app.Employee',
                                     verbose_name=_('Osoba decyzyjna'),
                                     on_delete=models.PROTECT,
                                     related_name="decision_user")

    class Meta:
        abstract = True
