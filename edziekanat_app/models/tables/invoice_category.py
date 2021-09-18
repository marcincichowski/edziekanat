from django.db import models


class InvoiceCategory(models.Model):
    name = models.CharField(max_length=70, unique=True)
    faq = models.URLField()
    short_desc = models.CharField(max_length=250)
    docx_template = models.FileField(upload_to="edziekanat_app/invoice_templates")
    template_location = models.FilePathField(editable=False, path="edziekanat_app/invoice_templates")

    def __str__(self):
        return self.name
