from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext as _


class InvoiceCategory(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=_('Nazwa'))

    faq_link = models.URLField(blank=True,
                               help_text="Link do regulaminu",
                               verbose_name=_('Regulamin'))

    description = RichTextField(verbose_name=_('Opis'),
                                blank=True)

    docx_template = models.FileField(upload_to="edziekanat_app/invoice_templates",
                                     verbose_name=_('Plik wzorcowy'))

    fields = dict()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.fields = document_parse(self.docx_template)

    class Meta:
        db_table = "edziekanat_app_invoices_categories"
        verbose_name = "Kategoria wniosku"
        verbose_name_plural = "Kategorie wniosków"

