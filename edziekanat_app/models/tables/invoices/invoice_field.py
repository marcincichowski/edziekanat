from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext as _


class InvoiceField(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=_('Nazwa'))

    description = RichTextField(verbose_name=_('Opis'),
                                blank=True)

    fields = dict()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        db_table = "edziekanat_app_invoice_fields"
        verbose_name = "Dziedzina wniosku"
        verbose_name_plural = "Dziedziny wniosków"

