from django.contrib import admin

from edziekanat_app.models.tables.course import Course
from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.invoice_field import InvoiceField
from edziekanat_app.models.tables.job import Job
from edziekanat_app.models.tables.subject import Subject
from edziekanat_app.models.tables.mode import Mode
from edziekanat_app.models.tables.specialization import Specialization
from edziekanat_app.models.tables.university_structure.chair import Chair
from edziekanat_app.models.tables.university_structure.department import Department
from edziekanat_app.models.tables.university_structure.faculty import Faculty
from edziekanat_app.models.tables.users.user import User
from edziekanat_app.models.tables.inbox.inbox import Inbox
from edziekanat_app.models.tables.messages.message import Message
from edziekanat_app.models.tables.users.student import Student
from edziekanat_app.models.tables.users.employee import Employee
from edziekanat_app.models.tables.users.admin import Admin

# Accounts
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Mode)
admin.site.register(Message)

# University Structure
admin.site.register(Department)
admin.site.register(Chair)
admin.site.register(Faculty)
admin.site.register(Job)

# Education
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Specialization)

# Invoices
admin.site.register(Invoice)
admin.site.register(InvoiceCategory)
admin.site.register(InvoiceField)
