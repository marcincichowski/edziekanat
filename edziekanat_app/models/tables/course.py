from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext as _

from edziekanat_app.models.tables.university_structure.faculty import Faculty


class Course(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=_('Nazwa'))

    deanery = models.ForeignKey(Faculty,
                                verbose_name=_('Wydział'),
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "edziekanat_app_invoices_courses"
        verbose_name = "Kierunek"
        verbose_name_plural = "Kierunki"
