from django.db import models
from django.utils.translation import gettext_lazy as _

class Invoice(models.Model):
    category = models.ForeignKey(to='edziekanat_app.InvoiceCategory',
                                 verbose_name=_('Kategoria'),
                                 on_delete=models.CASCADE)

    created_by = models.ForeignKey(to='edziekanat_app.User',
                                   verbose_name=_('Wnioskodawca'),
                                   on_delete=models.CASCADE,
                                   related_name="authors")

    invoice_file = models.FileField(verbose_name=_('Plik wniosku'),
                                    upload_to="edziekanat_app/docs")

    created_date = models.DateField(verbose_name=_('Data utworzenia'),
                                    auto_now=True,
                                    editable=False)

    status = models.CharField(verbose_name=_('Status wniosku'),
                              max_length=20,
                              default="W trakcie")

    decision_author = models.ForeignKey(to='edziekanat_app.User',
                                        verbose_name=_('Osoba wyznaczona do dokonania decyzji'),
                                        on_delete=models.PROTECT,
                                        related_name="decision_authors")

    decision = models.CharField(verbose_name=_('Decyzja'),
                                max_length=200,
                                blank=True)

    decision_file = models.FileField(verbose_name=_('Plik decyzji'),
                                     upload_to="edziekanat_app/docs")

    def __str__(self):
        return f"{self.name} - {self.status.lower()}"

    class Meta:
        db_table = "edziekanat_app_invoices"
        verbose_name = "Wniosek"
        verbose_name_plural = "Wnioski"
        unique_together = ['created_by', 'category', 'created_date']

