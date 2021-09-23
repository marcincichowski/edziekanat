import json

from braces.forms import UserKwargModelFormMixin
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.forms import *
from django.core.exceptions import ValidationError
from edziekanat_app.models.tables.course import Course
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.invoice_field import InvoiceField
from edziekanat_app.models.tables.specialization import Specialization
from edziekanat_app.models.tables.users.employee import Employee
from edziekanat_app.models.tables.users.role import Role
from edziekanat_app.models.tables.users.student import Student
from edziekanat_app.models.tables.job import Job
from edziekanat_app.models.tables.users.user import User


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
        dynamic_fields = json.loads(category.field_types)

        user = kwargs.pop('user')

        for key, value in dynamic_fields.items():
            if key.startswith('text'):
                self.fields[key] = CharField(
                    widget=PasswordInput(attrs={'class': 'input is-medium', 'label': value[3:]}))
            elif key.startswith('date'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[3:]}))
            elif key.startswith('phone'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[3:]}))
            elif key.startswith('value'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[3:]}))
            elif key.startswith('check'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[3:]}))
            elif key.startswith('select'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[3:]}))
            elif key.startswith('query'):
                value = get_query(value[3:], user)
                self.fields[key] = CharField(widget=HiddenInput(), initial=value)


class RegisterForm(Form):
    first_name = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Imię'}))
    last_name = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Nazwisko'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))
    password_repeat = CharField(
        widget=PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Powtórz hasło'}))
    role = ModelChoiceField(queryset=Role.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': 'Kim jesteś?'}))

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise ValidationError(u'Hasła różnią się!')


class RegisterExtraForm(UserKwargModelFormMixin, Form):
    address = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres zamieszkania'}))
    phone = CharField(widget=TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Telefon kontaktowy'}),
                      min_length=9,
                      max_length=9)

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role')
        super(RegisterExtraForm, self).__init__(*args, **kwargs)
        if role.name == Student.base_role:
            self.fields['course'] = ModelChoiceField(queryset=Course.objects.all(),
                                                     widget=Select(
                                                         attrs={'class': 'select', 'label': "Kierunek studiów"}))
            self.fields['specialization'] = ModelChoiceField(queryset=Specialization.objects.all(),
                                                             widget=Select(
                                                                 attrs={'class': 'select', 'label': "Specjalizacja"}),
                                                             required=False)
        if role.name == Employee.base_role:
            self.fields['job'] = ModelChoiceField(queryset=Job.objects.all(),
                                                  widget=Select(
                                                      attrs={'class': 'select', 'label': "Stanowisko"}),
                                                  required=False)


def get_query(queries: str, user: User):
    single_queries = queries.split('.')
    result = []

    if single_queries[0] == 'user':
        result.append(user)
    elif single_queries[0] == 'student':
        result.append(Student.objects.filter(user=user).first())
    else:
        raise Exception("Invalid base_object request!")

    single_queries = single_queries[1:]
    for request, i in zip(single_queries, range(len(single_queries))):
        base_object = result[i]
        response = getattr(base_object, request)
        if response is None:
            raise Exception(f"Unable to get response. Object: {base_object} Query: {request}")
        result.append(response)
    return result[-1]


class AddDictionaryValueCathedral(Form):
    value = CharField(
        widget=TextInput(attrs={'class': 'input is-primary is-fullwidth', 'placeholder': 'Nazwa katedry'}))

    def __init__(self, *args, **kwargs):
        super(AddDictionaryValueCathedral, self).__init__(*args, **kwargs)
        self.fields['value'].label = ""


class AddInvoiceCategory(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'placeholder': 'Nazwa kategorii'}))
    faq_link = CharField(widget=TextInput(attrs={'class': 'input', 'placeholder': 'FAQ link'}))
    description = CharField(widget=CKEditorWidget(attrs={'placeholder': 'Opis'}))
    docx_template = FileField(widget=ClearableFileInput(attrs={'class': 'file-input'}))
