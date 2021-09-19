from django.contrib import admin

from edziekanat_app.models.tables.admin import AdminMore
from edziekanat_app.models.tables.course import Course
from edziekanat_app.models.tables.employee import EmployeeMore
from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.role import Role
from edziekanat_app.models.tables.student import StudentMore
from edziekanat_app.models.tables.subject import Subject
from edziekanat_app.models.tables.university_structure.chair import Chair
from edziekanat_app.models.tables.university_structure.department import Department
from edziekanat_app.models.tables.university_structure.faculty import Faculty
from edziekanat_app.models.tables.user import User

# Accounts
admin.site.register(User)
admin.site.register(AdminMore)
admin.site.register(StudentMore)
admin.site.register(EmployeeMore)
admin.site.register(Role)

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
