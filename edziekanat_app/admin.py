from django.contrib import admin
from edziekanat_app.models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Institute)
admin.site.register(Subject)
admin.site.register(InvoiceCategory)
admin.site.register(Invoice)