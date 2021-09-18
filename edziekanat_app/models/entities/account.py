from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.user import User


class Account:
    def __init__(self, user: User):
        self.user = user
        self.invoices = get_user_invoices(user)
        print(self.invoices)

    def get_open_invoices(self): return self.invoices.filter(status="W trakcie")

    def get_closed_invoices(self): return self.invoices.filter(status="Zamknięte")

    def get_new_invoices(self): return self.invoices.filter(status="Nowy")


def get_user_invoices(user: User):
    try:
        return Invoice.objects.filter(created_by=user)
    except Invoice.DoesNotExist as err:
        print(f"Not found any [user ID:{user.id}]'s invoices")
        return Invoice.objects.none()
