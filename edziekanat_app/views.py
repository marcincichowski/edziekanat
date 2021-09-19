import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from edziekanat_app.models.entities.account import Account
from edziekanat_app.models.tables.users.base_user import User
from .forms import RegisterForm, LoginForm, AddDictionaryValueCathedral


def index(request, *args, **kwargs):
    if '_auth_user_id' not in request.session:
        return HttpResponseRedirect('login/')

    return render(request, 'index.html')


def invoices(request, *args, **kwargs):
    return render(request, 'user/invoices.html')


def administrators(request, *args, **kwargs):
    return render(request, 'admin/administrators.html')


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
    if '_auth_user_id' in request.session:
        return HttpResponseRedirect('/')

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

                return render(request, 'index.html')
            else:
                return render(request, 'auth/login.html', {
                    'form': form,
                    'message': 'Wprowadzono niepoprawne dane.'
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form, "time": datetime.datetime.now()})


def user_logout(request):
    if '_auth_user_id' in request.session:
        auth_logout(request)
    return HttpResponseRedirect('/')


class InvoiceCreator(SessionWizardView):
    template_name = "user/create_invoice.html"

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == '1':
            category = self.get_cleaned_data_for_step('0')['category']
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
                return render(request, template, {'message': 'Hasła nie zgadzają się.'})
            else:
                user = User.objects.create_user(
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email']
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
    if '_auth_user_id' in request.session:
        uid = request.session['_auth_user_id']
        user = User.objects.get(id=uid)
        return Account(user)
    else:
        return None


def session_context_processor(request):
    return {
        "time": datetime.datetime.now(),
        'acc': get_active_account(request)
    }

