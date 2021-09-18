import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

from edziekanat_app.models.entities.account import Account

from .forms import RegisterForm, LoginForm, AddDictionaryValueCathedral
from edziekanat_app.models.tables.invoice import Invoice
from edziekanat_app.models.tables.user import User


def index(request, *args, **kwargs):
    if '_auth_user_id' not in request.session:
        return HttpResponseRedirect('login/')

    return render(request, 'index.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def get_user_invoices(id):
    return filter(lambda x: x.created_by.id == id, Invoice.objects.all())


def invoices(request, *args, **kwargs):
    return render(request, 'user/invoices.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def administrators(request, *args, **kwargs):
    return render(request, 'admin/administrators.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def account(request, *args, **kwargs):
    return render(request, 'user/account.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def config(request, *args, **kwargs):
    return render(request, 'admin/config.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def settings(request, *args, **kwargs):
    return render(request, 'user/settings.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def get_invoice_creator(request):
    pass  # todo


def create_invoice(request, *args, **kwargs):
    return render(request, 'user/create_invoice.html', {
        'acc': get_active_account(request),
        'creator': get_invoice_creator(request),
        "time": datetime.datetime.now(),
    })


def dictionaries(request, *args, **kwargs):
    if request.method == 'GET':
        form = AddDictionaryValueCathedral()
        return render(request, 'admin/dictionaries.html', {
            'form': form,
            'acc': get_active_account(request),
            "time": datetime.datetime.now(),
        })
    elif request.method == 'POST':
        raise Exception("Not implemented")
        # check csrf !!!!
        return
    return render(request, 'admin/dictionaries.html', {
        'acc': get_active_account(request),
        "time": datetime.datetime.now(),
    })


def user_login(request):
    if '_auth_user_id' in request.session:
        return HttpResponseRedirect('/')

    template = 'auth/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print(f"Zalogowano:\n"
                      f"Email:{user.email}\n"
                      f"Hasło:{user.password}\n"
                      f"Imie:{user.first_name}\n"
                      f"Nazwisko:{user.last_name}")

                return render(request, 'index.html', {
                    'acc': get_active_account(request),
                    "time": datetime.datetime.now(),
                })
            else:
                return render(request, 'auth/login.html', {
                    'form': form,
                    "time": datetime.datetime.now(),
                    'message': 'Wprowadzono niepoprawne dane.'
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form, "time": datetime.datetime.now()})


def user_logout(request):
    if '_auth_user_id' in request.session:
        auth_logout(request)
    return HttpResponseRedirect('/')


def user_register(request):
    if '_auth_user_id' in request.session:
        return HttpResponseRedirect('/')

    template = 'auth/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    "time": datetime.datetime.now(),
                    "message": 'Konto z takim adresem e-mail już istnieje.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    "time": datetime.datetime.now(),
                    'message': 'Hasła nie zgadzają się.'
                })
            else:
                user = User.objects.create_user(
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['email']
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

                return render(request, 'index.html', {
                    'acc': get_active_account(request),
                    "time": datetime.datetime.now(),
                })

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
