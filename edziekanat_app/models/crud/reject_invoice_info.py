from dataclasses import dataclass

from django.db.models import FileField

from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.users.user import User

@dataclass
class RejectInvoiceInfo:
    category: InvoiceCategory
    created_by: User
    invoice_file: FileField
    created_date: str
    status: str
    decision_author: User
    decision: str