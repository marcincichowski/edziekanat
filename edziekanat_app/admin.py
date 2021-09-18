from django.contrib import admin
from edziekanat_app.models.tables.role import Role
from edziekanat_app.models.tables.user import User
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.institute import Institute


admin.site.register(User)
admin.site.register(Institute)
admin.site.register(InvoiceCategory)
admin.site.register(Invoice)
admin.site.register(Role)
