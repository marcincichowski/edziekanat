from django.db import models
from django.conf import settings
import os


class Institute(models.Model):
    name = models.CharField(max_length=70, unique=True)
    location = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Subject(models.Model):
    institution = models.ForeignKey(Institute, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    ects_points = models.IntegerField()
    sem = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['institution', 'name']


class User(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    acc_created_date = models.DateField(auto_now_add=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        abstract = True


class Employee(User):
    role = models.CharField(max_length=10)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)


class Student(User):
    indexNumber = models.CharField(unique=True, max_length=6)
    sem = models.IntegerField(default=1)


class InvoiceCategory(models.Model):
    name = models.CharField(max_length=70, unique=True)
    faq = models.URLField()
    short_desc = models.CharField(max_length=250)
    docx_template = models.FileField(upload_to="edziekanat_app/invoice_templates")
    template_location = models.FilePathField(editable=False, path="edziekanat_app/invoice_templates")

    def __str__(self):
        return self.name


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
        return f"{self.name} ({self.created_by.indexNumber}) - {self.status.lower()}"

