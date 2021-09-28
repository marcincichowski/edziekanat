import json
from dataclasses import dataclass
from django.db.models import FileField

from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.users.user import User


@dataclass
class RejectInvoiceInfo:
    category_name: str
    status: str
    decision_author: str
    decision: str
