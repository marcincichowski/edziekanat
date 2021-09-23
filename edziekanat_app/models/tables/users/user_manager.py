from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from edziekanat_app.models.tables.users.student import Student
from edziekanat_app.models.tables.users.admin import Admin
from edziekanat_app.models.tables.users.employee import Employee
from edziekanat_app.models.tables.users.role import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password, role, phone, address, allow_email_send=None, extra=None, **extra_fields):
        if not email:
            raise ValueError(_('E-mail nie może być pusty'))
        email = self.normalize_email(email)
        extra_fields.setdefault('role', role)
        extra_fields.setdefault('phone', phone)
        extra_fields.setdefault('address', address)
        extra_fields.setdefault('allow_email_send', allow_email_send)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        if role.name == Student.base_role:
            self.create_student(user, extra)
        if role.name == Admin.base_role:
            user.is_staff = True
            self.create_admin(user)
        if role.name == Employee.base_role:
            self.create_employee(user, extra)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', "Administrator")
        extra_fields.setdefault('last_name', "eDziekanat")
        extra_fields.setdefault('role', Role.objects.filter(name=Admin.base_role).first())

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def create_student(self, user, extra_fields):
        index=f'{user.id:06d}'
        course = extra_fields['course']
        Student(user=user,
                course=course,
                index=index).save()

    def create_admin(self, user):
        Admin(user=user).save()

    def create_employee(self, user, extra):
        job = extra['job']
        Employee(user=user,job=job).save()
