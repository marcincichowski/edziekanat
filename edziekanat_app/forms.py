import datetime
import json

from braces.forms import UserKwargModelFormMixin
from ckeditor.widgets import CKEditorWidget
from django.forms import *

from edziekanat_app.models.tables.course import Course
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.invoice_field import InvoiceField
from edziekanat_app.models.tables.job import Job
from edziekanat_app.models.tables.mode import Mode
from edziekanat_app.models.tables.specialization import Specialization
from edziekanat_app.models.tables.subject import Subject
from edziekanat_app.models.tables.university_structure.faculty import Faculty
from edziekanat_app.models.tables.users.employee import Employee
from edziekanat_app.models.tables.users.role import Role
from edziekanat_app.models.tables.users.student import Student
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

    def execute(self, method, **parameters):

        def get_subjects(user_id):
            student = Student.objects.filter(user_id=user_id).first()
            return Subject.objects.filter(course_id=student.course.id, sem=student.sem)

        methods = {'get_subjects': get_subjects}
        if parameters['user_id'] is not None:
            parameters['user_id'] = self.user.id
        return methods[method](**parameters)

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        super(InvoiceFillForm, self).__init__(*args, **kwargs)
        dynamic_fields = json.loads(category.field_types)

        user = kwargs.pop('user')

        checkboxes = {}
        label = ""

        for key, value in dynamic_fields.items():
            if key.startswith('text'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'textarea is-hovered', 'label': value[0][3:]}))
            elif key.startswith('areatext'):
                self.fields[key] = CharField(
                    widget=Textarea(attrs={'class': 'textarea', 'label': value[0][3:]}))
            elif key.startswith('date'):
                self.fields[key] = DateField(
                    widget=DateInput(attrs={'type': 'date', 'label': value[0][3:]}))
            elif key.startswith('phone'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[0][3:]}))
            elif key.startswith('value'):
                self.fields[key] = IntegerField(
                    widget=NumberInput(attrs={'class': 'input is-medium', 'label': value[0][3:]}))
            elif key.startswith('check'):
                self.fields[key] = CharField(
                    widget=TextInput(attrs={'class': 'input is-medium', 'label': value[0][3:]}))
            elif key.startswith('radio'):
                if len(checkboxes) == 0:
                    splitted = value[0][3:].split('|')
                    label = splitted[0]
                    checkboxes[key] = splitted[1]
                    self.fields[key] = ChoiceField(choices=checkboxes,
                                                   label=label,
                                                   widget=RadioSelect())
                else:
                    checkboxes[key] = value[0][3:]
            elif key.startswith('select'):
                splitted = value[0][3:].split(',')
                method = splitted[0]
                context = {}
                self.select_field = key
                for item in splitted[1:]:
                    params = item.split('?')
                    for param in params:
                        pairs = param.split('=')
                        context[pairs[0]] = pairs[1]
                choices = self.execute(method, **context)
                self.fields[key] = ModelChoiceField(queryset=choices,
                                                    widget=Select(
                                                        attrs={'class': 'select', 'placeholder': 'Przedmiot',
                                                               'label': 'Wybierz przedmiot'}))
                self.last_select_field = key
            elif key.startswith('file'):
                self.fields[key] = FileField(
                    widget=FileInput(
                        attrs={'class': 'file-input', 'type': 'file', 'label': value[0][3:], 'name': 'resume'}),
                    required=True)
            elif key.startswith('result'):
                value = f"{self.last_select_field}.{value[0][3:]}"
                self.fields[key] = CharField(widget=HiddenInput(), initial=value)
            elif key.startswith('query'):
                value = get_query(value[0][3:], user)
                self.fields[key] = CharField(widget=HiddenInput(), initial=value)


def bind(init):
    results = {}
    for k in init:
        results.setdefault(k, []).append(init[k])
    return results


def get_query(queries, user: User, base=None):
    single_queries = queries.split('.')
    result = []

    if base is None:
        if single_queries[0] == 'user':
            result.append(user)
        elif single_queries[0] == 'student':
            result.append(Student.objects.filter(user=user).first())
        elif single_queries[0] == 'system':
            if single_queries[1] == 'today':
                return datetime.datetime.today().strftime('%d.%m.%Y') + " r."
            if single_queries[1] == 'study_session':
                start = (3, 1)
                end = (9, 3)
                if start < (datetime.date.today().month, datetime.date.today().day) < end:
                    return "letniej"
                else:
                    return "zimowej"
        else:
            raise Exception(f"Invalid base_object request: {single_queries[0]}")
    else:
        result.append(base)

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


class RejectInvoiceForm(Form):
    decision = CharField(widget=Textarea(attrs={'class': 'textarea', 'label': "Decyzja"}))
    status = CharField(widget=HiddenInput(), initial='Odrzucony')
    id = CharField(widget=HiddenInput())


class AcceptInvoiceForm(Form):
    id_accept = CharField(widget=HiddenInput())


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
    birth_date = DateField(widget=DateInput(attrs={'type': 'date', 'label': 'Data urodzenia'}))

    allow_email_send = BooleanField(
        widget=CheckboxInput(attrs={'class': 'required checkbox form-control', 'label': "Zgoda na korespondencję"}),
        initial=True)

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


class AddInvoiceCategory(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'placeholder': 'Nazwa kategorii'}))
    faq_link = CharField(widget=TextInput(attrs={'class': 'input', 'placeholder': 'FAQ link'}))
    description = CharField(widget=CKEditorWidget(attrs={'placeholder': 'Opis'}))
    docx_template = FileField(widget=ClearableFileInput(attrs={'class': 'file-input'}))


class SystemTools(Form):
    smtp_address = CharField(
        widget=TextInput(attrs={'class': 'input', 'placeholder': '10.124.14.1:25', 'label': 'Adres IP serwera SMTP'}),
        initial='')
    broadcast = CharField(
        widget=Textarea(attrs={'class': 'textarea', 'label': 'Wyślij komunikat do wszystkich użytkowników'}))


# -------------------------------------------- DATABASE FORMS -------------------------------------------- #

class AddAdministrator(Form):
    name = ModelChoiceField(queryset=User.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Kierownik katedry"}),
                            required=True)

class AddChair(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa katedry'}))
    location = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Adres katedry'}))

    head = ModelChoiceField(queryset=Employee.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Kierownik katedry"}),
                            required=True)

    contact_user = ModelChoiceField(queryset=Employee.objects.all(),
                                    widget=Select(attrs={'class': 'select', 'label': "Osoba kontaktowa"}),
                                    required=True)


class AddCourse(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa kierunku'}))

    department = ModelChoiceField(queryset=Faculty.objects.all(),
                                  widget=Select(attrs={'class': 'select', 'label': "Wydział"}),
                                  required=True)

    degree = IntegerField(widget=NumberInput(attrs={'class': 'input is-medium', 'label': 'Stopień studiów'}))

    mode = ModelChoiceField(queryset=Mode.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Tryb studiów"}),
                            required=True)


class AddDepartment(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa instytutu'}))
    location = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Adres instytutu'}))

    head = ModelChoiceField(queryset=Employee.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Dyrektor instytutu"}),
                            required=True)

    contact_user = ModelChoiceField(queryset=Employee.objects.all(),
                                    widget=Select(attrs={'class': 'select', 'label': "Osoba kontaktowa"}),
                                    required=True)


class AddEmployee(Form):
    job = ModelChoiceField(queryset=Job.objects.all(),
                           widget=Select(attrs={'class': 'select', 'label': "Zawód"}),
                           required=True)

    user = ModelChoiceField(queryset=User.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Użytkownik"}),
                            required=True)

    boss = ModelChoiceField(queryset=User.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Szef"}),
                            required=True)


class AddFaculty(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa wydziału'}))
    location = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Adres wydziału'}))

    head = ModelChoiceField(queryset=Employee.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Dziekan"}),
                            required=True)

    contact_user = ModelChoiceField(queryset=Employee.objects.all(),
                                    widget=Select(attrs={'class': 'select', 'label': "Osoba kontaktowa"}),
                                    required=True)


class AddIncoiceCategories(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa wniosku'}))
    faq_link = URLField(label='URL', required=False)
    description = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Opis'}))
    field_type = CharField(widget=TextInput(attrs={'class': 'input'}))
    field = ModelChoiceField(queryset=InvoiceField.objects.all(),
                             widget=Select(attrs={'class': 'select', 'label': "Dziedzina"}),
                             required=True)
    decision_query = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Decyzja'}))


class AddInvoiceField(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa kategorii'}))
    description = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Opis'}))


class AddInvoice(Form):
    invoice_file = FileField(
        widget=FileInput(
            attrs={'class': 'file-input', 'type': 'file', 'label': 'Wniosek', 'name': 'Plik'}),
        required=True)
    created_date = DateField(widget=DateInput(attrs={'type': 'date', 'label': 'Data utworzenia wniosku'}))
    status = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Status'}))
    decision = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Decyzja'}))
    category = ModelChoiceField(queryset=InvoiceCategory.objects.all(),
                                widget=Select(attrs={'class': 'select', 'label': "Kategoria"}),
                                required=True)
    created_by = ModelChoiceField(queryset=User.objects.all(),
                                  widget=Select(attrs={'class': 'select', 'label': "Twórca wniosku"}),
                                  required=True)
    decision_author = ModelChoiceField(queryset=User.objects.all(),
                                       widget=Select(attrs={'class': 'select', 'label': "Autor decyzji"}),
                                       required=True)


class AddJob(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa stanowiska'}))


class AddRole(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa roli'}))


class AddSpectialization(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa specjalizacji'}))
    course = ModelChoiceField(queryset=Course.objects.all(),
                              widget=Select(attrs={'class': 'select', 'label': "Kierunek"}),
                              required=True)


class AddStudent(Form):
    index = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Numer indexu'}))
    sem = IntegerField(widget=NumberInput(attrs={'class': 'input is-medium', 'label': 'Semestr'}))
    course = ModelChoiceField(queryset=Course.objects.all(),
                              widget=Select(attrs={'class': 'select', 'label': "Kierunek"}),
                              required=True)
    spectialization = ModelChoiceField(queryset=Specialization.objects.all(),
                                       widget=Select(attrs={'class': 'select', 'label': "Specjalizacja"}),
                                       required=True)
    user = ModelChoiceField(queryset=User.objects.all(),
                            widget=Select(attrs={'class': 'select', 'label': "Użytkownik"}),
                            required=True)
    academic_year = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Rok akademicki'}))


class AddStudyMode(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa'}))


class AddSubject(Form):
    name = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Nazwa'}))
    ects = IntegerField(widget=NumberInput(attrs={'class': 'input is-medium', 'label': 'ECTS'}))
    sem = IntegerField(widget=NumberInput(attrs={'class': 'input is-medium', 'label': 'Semestr'}))
    teacher = ModelChoiceField(queryset=Employee.objects.all(),
                               widget=Select(attrs={'class': 'select', 'label': "Prowadzący"}),
                               required=True)
    course = ModelChoiceField(queryset=Course.objects.all(),
                              widget=Select(attrs={'class': 'select', 'label': "Kierunek"}),
                              required=True)
    type = CharField(widget=TextInput(attrs={'class': 'input', 'label': 'Rodzaj zajęć'}))

