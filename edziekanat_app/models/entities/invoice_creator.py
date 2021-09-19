from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.invoice_category import InvoiceCategory


class InvoiceCreator:
    def __init__(self):
        self.categories = InvoiceCategory.objects.all()
        self.invoices = Invoice.objects.all()

    def get_invoices_from_category(self, category: InvoiceCategory):
        try:
            return self.invoices.filter(category=category)
        except Invoice.DoesNotExist:
            return Invoice.objects.none()
