from django.db import models
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.student import Student


class Invoice(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(InvoiceCategory, on_delete=models.CASCADE)

    create_date = models.DateField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    last_modified = models.DateField(auto_now=True, editable=False)

    status = models.CharField(max_length=20, default="W trakcie")
    decision = models.CharField(max_length=200, blank=True)

    uploaded = models.BooleanField(editable=False, default=False)
    file = models.FileField(upload_to="edziekanat_app/docs")
    file_location = models.FilePathField(editable=False, path="edziekanat_app/docs")

    def __str__(self):
        return f"{self.name} - {self.status.lower()}"
