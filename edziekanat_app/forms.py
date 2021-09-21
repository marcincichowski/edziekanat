import json

from braces.forms import UserKwargModelFormMixin
from django.forms import *

from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.invoice_field import InvoiceField
from edziekanat_app.models.tables.users.role import Role


class RegisterForm(Form):
    first_name = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Imię'}))
    last_name = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Nazwisko'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))
    password_repeat = CharField(
        widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Powtórz hasło'}))
    role = ModelChoiceField(queryset=Role.objects.all(), widget=Select(attrs={'class': 'select'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)


class EditUserForm(Form):
    user_id = CharField(widget=HiddenInput())
    first_name = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Imię'}))
    last_name = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Nazwisko'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))
    password_repeat = CharField(
        widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Powtórz hasło'}))
    role = ModelChoiceField(queryset=Role.objects.all(),
                            widget=Select(attrs={'class': 'select', 'placeholder': 'Rola'}))


class LoginForm(Form):
    email = EmailField(widget=EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))


class InvoiceFieldPickForm(Form):
    field = ModelChoiceField(queryset=InvoiceField.objects.all(),
                             widget=Select(attrs={'placeholder': 'Dziedzina wniosku'}))


class InvoiceCategoryPickForm(UserKwargModelFormMixin, ModelForm):
    class Meta:
        model = InvoiceCategory
        fields = ['category']

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories')
        super(InvoiceCategoryPickForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = categories

    category = ModelChoiceField(queryset=InvoiceCategory.objects.all())


class InvoiceFillForm(UserKwargModelFormMixin, Form):

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        super(InvoiceFillForm, self).__init__(*args, **kwargs)
        invoice_fields = json.loads(category.field_types)
        self.set_up_fields(invoice_fields)

    def set_up_fields(self, invoice_fields):
        for type, fields in invoice_fields.items():
            for i in range(0, len(invoice_fields[type.upper()])):
                label = fields[f"field_{i}"]
                self.fields[f"{type.lower()}_field_{i}"] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': label}))


class AddDictionaryValueCathedral(Form):
    value = CharField(
        widget=TextInput(attrs={'class': 'input is-primary is-fullwidth', 'placeholder': 'Nazwa katedry'}))

    def __init__(self, *args, **kwargs):
        super(AddDictionaryValueCathedral, self).__init__(*args, **kwargs)
        self.fields['value'].label = ""
