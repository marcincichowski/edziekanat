from django.contrib import admin

from edziekanat_app.models.tables.course import Course
from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.subject import Subject
from edziekanat_app.models.tables.university_structure.chair import Chair
from edziekanat_app.models.tables.university_structure.department import Department
from edziekanat_app.models.tables.university_structure.faculty import Faculty
from edziekanat_app.models.tables.users.user import User
from edziekanat_app.models.tables.users.student import Student
from edziekanat_app.models.tables.users.employee import Employee

# Accounts
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Employee)

# University Structure
admin.site.register(Department)
admin.site.register(Chair)
admin.site.register(Faculty)

# Education
admin.site.register(Course)
admin.site.register(Subject)

# Invoices
admin.site.register(Invoice)
admin.site.register(InvoiceCategory)
