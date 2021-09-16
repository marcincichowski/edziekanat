from django.db import models
from django.conf import settings
import os
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django import forms

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

class Role(models.Model):
    STUDENT = 1
    TEACHER = 2
    SECRETARY = 3
    SUPERVISOR = 4
    ADMIN = 5
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (SECRETARY, 'secretary'),
        (SUPERVISOR, 'supervisor'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "Student"
        EMPLOYEE = "Employee"
        SUPERVISOR = "Supervisor"
        ADMIN = "Admin"

    role = models.CharField(_("Role"), max_length=50, choices=Roles.choices, default=Roles.STUDENT)

    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    acc_created_date = models.DateField(auto_now_add=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(_('password'), max_length=128)

    def __str__(self):
        return f"{self.name} {self.surname} {self.id}"


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.STUDENT)

class StudentMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.STUDENT
        return super().save()

class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.EMPLOYEE)


class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.EMPLOYEE
        return super().save()


class SupervisorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.SUPERVISOR)


class Supervisor(User):
    objects = SupervisorManager()

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.SUPERVISOR
        return super().save()


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.ADMIN)


class Admin(User):

    class Meta:
        proxy = True

    def save(self):
        if not self.pk:
            self.role = User.Roles.ADMIN
        return super().save()


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


