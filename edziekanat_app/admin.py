from django.contrib import admin
from edziekanat_app.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Institute)
admin.site.register(InvoiceCategory)
admin.site.register(Invoice)
admin.site.register(Role)
