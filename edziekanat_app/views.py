import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import auth_logout
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from docx import Document
from formtools.wizard.views import SessionWizardView

from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.invoice_category import replace_document_tags
from edziekanat_app.models.tables.users.employee import Employee
from edziekanat_app.models.tables.users.student import Student
from edziekanat_app.models.tables.users.user import User
from .forms import RegisterForm, LoginForm, AddDictionaryValueCathedral, EditUserForm
from .models.tables.invoice_category import InvoiceCategory


def index(request, *args, **kwargs):
    context = {
        'open_invoices': get_open_invoices(request.user),
        'closed_invoices': get_closed_invoices(request.user),
        'new_invoices': get_new_invoices(request.user),
        'all_invoices': get_user_invoices(request.user)
    }
    return render(request, 'index.html', context=context)


def invoices(request, *args, **kwargs):
    invoices = InvoiceCategory.objects.all()
    return render(request, 'user/invoices.html', context={'invoices': invoices})


def invoices_list_details(request, *args, **kwargs):
    if request.method == 'GET' and request.is_ajax():
        id = request.GET.get('id', None)
        if Invoice.objects.filter(id=id).exists():
            return JsonResponse({'Valid': True, 'data': serialize('json', Invoice.objects.filter(id=id))}, status=200)
        else:
            return JsonResponse({'Valid': False}, status=200)

    return JsonResponse({}, status=400)


def invoices_list(request, *args, **kwargs):
    invoices = Invoice.objects.filter(created_by=request.user)
    return render(request, 'user/invoices_list.html', context={'invoices': invoices})


def administrators(request, *args, **kwargs):
    users = User.objects.all()
    edit_form = EditUserForm()
    return render(request, 'admin/administrators.html', context={'users': users, 'form': edit_form})


def account(request, *args, **kwargs):
    return render(request, 'user/account.html')


def config(request, *args, **kwargs):
    return render(request, 'admin/config.html')


def settings(request, *args, **kwargs):
    return render(request, 'user/settings.html')


def create_invoice(request, *args, **kwargs):
    return render(request, 'user/create_invoice.html')


def dictionaries(request, *args, **kwargs):
    if request.method == 'GET':
        form = AddDictionaryValueCathedral()
        return render(request, 'admin/dictionaries.html', {'form': form})
    elif request.method == 'POST':
        raise Exception("Not implemented")
        # check csrf !!!!
        return
    return render(request, 'admin/dictionaries.html')


def user_login(request):
    template = 'auth/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print(f"Zalogowano:\n"
                      f"Email:{user.email}\n"
                      f"Hasło:{user.password}\n"
                      f"Imie:{user.first_name}\n"
                      f"Nazwisko:{user.last_name}")

                return redirect('/')
            else:
                return render(request, 'auth/login.html', {
                    'form': form,
                    'message': 'Wprowadzono niepoprawne dane.'
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form, "time": datetime.datetime.now()})


def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


class InvoiceCreator(SessionWizardView):
    template_name = "user/create_invoice.html"
    file_storage = FileSystemStorage(location='invoices/')

    def get_form_kwargs(self, step=None):
        self.extra_context = {'title': 'Wybierz dziedzinę wniosku'}
        kwargs = {}
        if step == '1':
            field = self.get_cleaned_data_for_step('0')['field']
            queryset = InvoiceCategory.objects.filter(field=field)
            kwargs.update({'categories': queryset, })
            self.extra_context.update({'title': "Wybierz kategorię wniosku"})
        if step == '2':
            category = self.get_cleaned_data_for_step('1')['category']
            kwargs.update({'category': category, 'user': self.request.user})
            self.extra_context.update({'title': "Wybrany wniosek", 'category_name': category.name})
        return kwargs

    def done(self, form_list, **kwargs):
        category = self.get_cleaned_data_for_step('1')['category']

        result = form_list[2].cleaned_data
        attachement = None  # not handling attachements yet

        for key in result:
            if key.startswith('file'):
                attachement = result[key]
                result[key] = result[key].name


        inv = Invoice.objects.create(category=category,
                                     created_by=self.request.user,
                                     created_date=datetime.datetime.now(),
                                     decision_author=self.request.user)  # todo
        try:
            doc = Document(category.docx_template.path)
            new_invoice_file_path = f"edziekanat_app/invoices/{category.name.replace(' ', '_')}_ID_{inv.id}.docx"
            replace_document_tags(doc, result, init=False).save(new_invoice_file_path)
            file = File(open(new_invoice_file_path, 'rb'))
            inv.invoice_file.save(name=attachement.name, content=file)
        except Exception as e:
            inv.delete()
            raise Exception(e.__str__())

        return HttpResponseRedirect('/')


class UserCreator(SessionWizardView):
    template_name = "auth/register.html"

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == '1':
            role = self.get_cleaned_data_for_step('0')['role']
            kwargs.update({'role': role, })
        return kwargs

    def done(self, form_list, **kwargs):
        email = self.get_cleaned_data_for_step('0')['email']
        password = self.get_cleaned_data_for_step('0')['password']
        password_repeat = self.get_cleaned_data_for_step('0')['password_repeat']
        role = self.get_cleaned_data_for_step('0')['role']
        first_name = self.get_cleaned_data_for_step('0')['first_name']
        last_name = self.get_cleaned_data_for_step('0')['last_name']
        address = self.get_cleaned_data_for_step('1')['address']
        phone = self.get_cleaned_data_for_step('1')['phone']
        birth_date = self.get_cleaned_data_for_step('1')['birth_date']
        allow_email_send = self.get_cleaned_data_for_step('1')['allow_email_send']

        if User.objects.filter(email=email).exists():
            raise ValidationError('Użytkownik o takim adresie e-mail już istnieje.')
        elif password != password_repeat:
            raise ValidationError('Hasła nie zgadzają się.')
        else:
            extra = {}
            if role.name == Student.base_role:
                extra = {
                    'course': self.get_cleaned_data_for_step('1')['course'],
                    'specialization': self.get_cleaned_data_for_step('1')['specialization'],
                }
            if role.name == Employee.base_role:
                extra = {
                    'job': self.get_cleaned_data_for_step('1')['job']
                }
            user = User.objects.create_user(
                password=password,
                email=email,
                role=role,
                phone=phone,
                address=address,
                birth_date=birth_date,
                allow_email_send=allow_email_send,
                extra=extra
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print(f"Zarejestrowano:\n"
                  f"Email:{user.email}\n"
                  f"Hasło:{user.password}\n"
                  f"Imie:{user.first_name}\n"
                  f"Nazwisko:{user.last_name}")
            login(self.request, user)
        return HttpResponseRedirect('/')


def user_register(request):
    if '_auth_user_id' in request.session:
        return HttpResponseRedirect('/')

    template = 'auth/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)


    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


def session_context_processor(request):
    return {
        "time": datetime.datetime.now()
    }


def get_open_invoices(user: User): return Invoice.objects.filter(status="W trakcie", created_by=user)


def get_closed_invoices(user: User): return Invoice.objects.filter(status="Zamknięte", created_by=user)


def get_new_invoices(user: User): return Invoice.objects.filter(status="Nowy", created_by=user)


def get_user_invoices(user: User): return Invoice.objects.filter(created_by=user)
