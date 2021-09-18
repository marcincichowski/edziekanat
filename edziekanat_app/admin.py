from django.contrib import admin
from edziekanat_app.models.role import Role
from edziekanat_app.models.user import User
from edziekanat_app.models.invoice_category import InvoiceCategory
from edziekanat_app.models.invoice import Invoice
from edziekanat_app.models.institute import Institute


admin.site.register(User)
admin.site.register(Institute)
admin.site.register(InvoiceCategory)
admin.site.register(Invoice)
admin.site.register(Role)
