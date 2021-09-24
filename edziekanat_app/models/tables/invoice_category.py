import json
import re
import jinja2
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db.models import *
from django.utils.translation import gettext as _
from docx import Document

BASE_PATTERN = r'(?s)(?<={{).*?(?=}})'
PATTERNS = {
    'TEXT': 'TEX',
    'AREATEXT': 'ARE',
    'DATE': 'DAT',
    'PHONE': 'PHO',
    'VALUE': 'VAL',
    'CHECK': 'CHE',
    'SELECT': 'SEL',
    'FILE': 'FIL',
    'QUERY': 'QUE'
}


def regex_result_to_dict(lst):
    result = dict()
    for i in range(len(lst)):
        field_type = get_field_type(lst[i])
        result[f'{field_type}_field_{i}'] = lst[i]
    return result


def find_pattern(text, pattern): return re.findall(pattern, text)


def get_field_type(item: str):
    return {
        PATTERNS['TEXT']: 'text',
        PATTERNS['AREATEXT']: 'areatext',
        PATTERNS['DATE']: 'text',
        PATTERNS['PHONE']: 'text',
        PATTERNS['VALUE']: 'text',
        PATTERNS['CHECK']: 'check',
        PATTERNS['FILE']: 'file',
        PATTERNS['QUERY']: 'query'
    }[item[0:3]]


class InvoiceCategory(Model):

    def validate_file_extension(value):
        if not value.name.endswith('.docx'):
            raise ValidationError(u'Plik musi mieć rozszerzenie .docx')

    name = CharField(max_length=100,
                     unique=True,
                     verbose_name=_('Nazwa'))

    decision_query = CharField(max_length=100,
                               default="NONE",
                               verbose_name=_('Query osoby wyznaczającej'))

    field = ForeignKey(to='edziekanat_app.InvoiceField',
                       verbose_name=_('Dziedzina'),
                       on_delete=CASCADE, default=None, null=None)

    faq_link = URLField(blank=True,
                        help_text="Link do regulaminu",
                        verbose_name=_('Regulamin'))

    description = RichTextField(verbose_name=_('Opis'),
                                blank=True)

    docx_template = FileField(upload_to="edziekanat_app/invoice_templates",
                              verbose_name=_('Plik wzorcowy'),
                              validators=[validate_file_extension])

    dynamic_fields = {}

    field_types = CharField(max_length=1000, default=json.dumps(dynamic_fields), editable=False)

    def set_field_types(self, x):
        self.field_types = json.dumps(x)

    def get_field_types(self):
        return json.loads(self.field_types)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.document_parse()

        super(InvoiceCategory, self).save()

    class Meta:
        db_table = "edziekanat_app_invoice_categories"
        verbose_name = "Kategoria wniosku"
        verbose_name_plural = "Kategorie wniosków"

    def document_parse(self):
        doc = Document(self.docx_template.path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        concatted_text = '\n'.join(text)

        matches = find_pattern(concatted_text, BASE_PATTERN)
        result = regex_result_to_dict(matches)
        self.set_field_types(result)
        replace_document_tags(doc, result, self.docx_template.path)


def replace_document_tags(doc: Document, dictionary: dict, save_path: str, final: bool = False):
    for i in dictionary:
        for p in doc.paragraphs:
            test =  '{{' + f"{dictionary[i]}" + '}}' if final else dictionary[i]
            matches = p.text.find(test)
            if matches >= 0:
                p.text = p.text.replace(test, "{{" + i + "}}")
    doc.save(save_path)

