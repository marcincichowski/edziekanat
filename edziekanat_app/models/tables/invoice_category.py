import json
import re

from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from docx import Document


class InvoiceCategory(models.Model):
    PATTERNS = {
        'TEXT': r'(?s)(?<={{).*?(?=}})',
        'DATE': r'(?s)(?<={_{).*?(?=}_})',
        'PHONE': r'(?s)(?<={#{).*?(?=}#})',
        'VALUE': r'(?s)(?<={${).*?(?=}$})'
    }

    def validate_file_extension(value):
        if not value.name.endswith('.docx'):
            raise ValidationError(u'Plik musi mieć rozszerzenie .docx')

    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=_('Nazwa'))

    field = models.ForeignKey(to='edziekanat_app.InvoiceField',
                              verbose_name=_('Dziedzina'),
                              on_delete=models.CASCADE, default=None, null=None)

    faq_link = models.URLField(blank=True,
                               help_text="Link do regulaminu",
                               verbose_name=_('Regulamin'))

    description = RichTextField(verbose_name=_('Opis'),
                                blank=True)

    docx_template = models.FileField(upload_to="edziekanat_app/invoice_templates",
                                     verbose_name=_('Plik wzorcowy'),
                                     validators=[validate_file_extension])

    dynamic_fields = {
        'TEXT': dict(),
        'DATE': dict(),
        'PHONE': dict(),
        'VALUE': dict(),
    }

    field_types = models.CharField(max_length=1000, default=json.dumps(dynamic_fields), editable=False)

    def set_field_types(self, x):
        self.field_types = json.dumps(x)

    def get_field_types(self):
        return json.loads(self.field_types)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.document_parse(self.docx_template.path)
        super(InvoiceCategory, self).save()

    class Meta:
        db_table = "edziekanat_app_invoice_categories"
        verbose_name = "Kategoria wniosku"
        verbose_name_plural = "Kategorie wniosków"

    def document_parse(self, path):
        doc = Document(path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        concatted_text = '\n'.join(text)

        result = {
            'TEXT': self.regex_result_to_dict(find_pattern(concatted_text, self.PATTERNS['TEXT'])),
            'DATE': self.regex_result_to_dict(find_pattern(concatted_text, self.PATTERNS['DATE'])),
            'PHONE': self.regex_result_to_dict(find_pattern(concatted_text, self.PATTERNS['PHONE'])),
            'VALUE': self.regex_result_to_dict(find_pattern(concatted_text, self.PATTERNS['VALUE']))
        }
        self.set_field_types(result)

    def regex_result_to_dict(self, lst):
        result = dict()
        for i in range(len(lst)):
            result[f'field_{i}'] = lst[i]
        return result


def find_pattern(text, pattern): return re.findall(pattern, text)
