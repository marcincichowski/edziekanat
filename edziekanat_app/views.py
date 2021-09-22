import datetime
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import auth_logout
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView

from edziekanat_app.models.tables.invoice import Invoice
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

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == '1':
            field = self.get_cleaned_data_for_step('0')['field']
            queryset = InvoiceCategory.objects.filter(field=field)
            kwargs.update({'categories': queryset, })
        if step == '2':
            category = self.get_cleaned_data_for_step('1')['category']
            kwargs.update({'category': category, })
        return kwargs

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/')


def user_register(request):
    if '_auth_user_id' in request.session:
        return HttpResponseRedirect('/')

    template = 'auth/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    "message": 'Konto z takim adresem e-mail już istnieje.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {'form': form,
                                                  'message': 'Hasła nie zgadzają się.'})
            else:
                user = User.objects.create_user(
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    role=form.cleaned_data['role']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                print(f"Zarejestrowano:\n"
                      f"Email:{user.email}\n"
                      f"Hasło:{user.password}\n"
                      f"Imie:{user.first_name}\n"
                      f"Nazwisko:{user.last_name}")

                login(request, user)

                return render(request, 'index.html')

    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


def get_active_account(request):
    if request.user.is_authenticated:
        return Account(request.user)
    else:
        return None


def session_context_processor(request):
    return {
        "time": datetime.datetime.now()
    }


def get_open_invoices(user: User): return Invoice.objects.filter(status="W trakcie", created_by=user)


def get_closed_invoices(user: User): return Invoice.objects.filter(status="Zamknięte", created_by=user)


def get_new_invoices(user: User): return Invoice.objects.filter(status="Nowy", created_by=user)


def get_user_invoices(user: User): return Invoice.objects.filter(created_by=user)
