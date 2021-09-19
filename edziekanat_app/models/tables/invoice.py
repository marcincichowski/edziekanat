from django.db import models
from django.utils.translation import gettext_lazy as _

from edziekanat_app.models.tables.employee import Employee
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.student import Student


class Invoice(models.Model):
    category = models.ForeignKey(InvoiceCategory,
                                 verbose_name=_('Kategoria'),
                                 on_delete=models.CASCADE)

    created_by = models.ForeignKey(Student,
                                   verbose_name=_('Wnioskodawca'),
                                   on_delete=models.CASCADE,
                                   related_name="authors",
                                   editable=False)

    created_date = models.DateField(verbose_name=_('Data utworzenia'),
                                    auto_now=True,
                                    editable=False)

    status = models.CharField(verbose_name=_('Status wniosku'),
                              max_length=20,
                              default="W trakcie")

    decision = models.CharField(verbose_name=_('Decyzja'),
                                max_length=200,
                                blank=True, )

    decision_file = models.FileField(verbose_name=_('Plik decyzji'),
                                     upload_to="edziekanat_app/docs")

    decision_file_location = models.FilePathField(verbose_name=_('Lokalizacja pliku decyzji'),
                                                  editable=True,
                                                  path="edziekanat_app/invoice_decisions")

    decision_author = models.ForeignKey(Employee,
                                        verbose_name=_('Osoba wyznaczona do dokonania decyzji'),
                                        on_delete=models.PROTECT,
                                        related_name="decision_authors")

    invoice_file = models.FileField(verbose_name=_('Plik wniosku'),
                                    upload_to="edziekanat_app/docs",
                                    editable=False)

    invoice_file_location = models.FilePathField(verbose_name=_('Lokalizacja wniosku'),
                                                 editable=False,
                                                 path="edziekanat_app/docs")

    def __str__(self):
        return f"{self.name} - {self.status.lower()}"

    class Meta:
        db_table = "edziekanat_app_invoices"
        verbose_name = "Wniosek"
        verbose_name_plural = "Wnioski"
        unique_together = ['created_by', 'category', 'created_date']
