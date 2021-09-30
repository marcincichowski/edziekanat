from dataclasses import dataclass


@dataclass
class RejectInvoiceInfo:
    category_name: str
    status: str
    decision_author: str
    decision: str
