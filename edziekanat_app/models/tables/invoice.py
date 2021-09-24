from django.db.models import *
from django.utils.translation import gettext_lazy as _


class Invoice(Model):
    category = ForeignKey(to='edziekanat_app.InvoiceCategory',
                          verbose_name=_('Kategoria'),
                          on_delete=CASCADE)

    created_by = ForeignKey(to='edziekanat_app.User',
                            verbose_name=_('Wnioskodawca'),
                            on_delete=CASCADE,
                            related_name="authors")

    invoice_file = FileField(verbose_name=_('Plik wniosku'),
                             upload_to="edziekanat_app/docs",
                             null=True,
                             blank=True)

    created_date = DateField(verbose_name=_('Data utworzenia'),
                             auto_now=True,
                             editable=False)

    status = CharField(verbose_name=_('Status wniosku'),
                       max_length=20,
                       default="W trakcie")

    decision_author = ForeignKey(to='edziekanat_app.User',
                                 verbose_name=_('Osoba wyznaczona do dokonania decyzji'),
                                 on_delete=PROTECT,
                                 related_name="decision_authors")

    decision = CharField(verbose_name=_('Decyzja'),
                         max_length=200,
                         blank=True)

    decision_file = FileField(verbose_name=_('Plik decyzji'),
                              upload_to="edziekanat_app/docs",
                              blank=True)

    def __str__(self):
        return f"{self.status}"

    class Meta:
        db_table = "edziekanat_app_invoices"
        verbose_name = "Wniosek"
        verbose_name_plural = "Wnioski"
        unique_together = ['created_by_id', 'category_id', 'created_date']
