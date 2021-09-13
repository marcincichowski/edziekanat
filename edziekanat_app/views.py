from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from edziekanat_app.models import Invoice
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm
import datetime
import threading
import time


def index(request, *args, **kwargs):
    get_session(request)
    form = LoginForm(request.POST)
    context = {
        "form": form,
        "time": datetime.datetime.now(),
        "logged_in": False
    }
    return render(request, 'edziekanat_app/index.html', {'user_count': User.objects.count(),
                                                                    'document_count': Invoice.objects.count(),
                                                                    "time": datetime.datetime.now()})



def user_login(request):
    template = 'edziekanat_app/user/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return render(request, 'edziekanat_app/index.html', {'user_count': User.objects.count(),
                                                                    'document_count': Invoice.objects.count(),
                                                                    "time": datetime.datetime.now()})
            else:
                return render(request, 'edziekanat_app/user/login.html',{
                    'form': form,
                    "time": datetime.datetime.now(),
                    'error_message': 'Wprowadzono niepoprawne dane.'
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form, "time": datetime.datetime.now()})


def user_register(request):
    template = 'edziekanat_app/user/register.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    "time": datetime.datetime.now(),
                    "error_message": 'Konto z takim adresem e-mail już istnieje.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    "time": datetime.datetime.now(),
                    'error_message': 'Hasła nie zgadzają się.'
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
                print(f"Email:{user.email}\nHasło:{user.password}\nImie:{user.first_name}\nNazwisko:{user.last_name}")
                login(request, user)
                set_session(request, user)
                get_session(request)
                return render(request, 'edziekanat_app/index.html', {
                    'user_count': User.objects.count(),
                    'document_count': Invoice.objects.count(),
                    "time": datetime.datetime.now(),
                })

    else:
        form = RegisterForm()

    return render(request, template, {'form': form})

def set_session(request, user: User):
    request.session['email'] = user.email
    print("SESJA SET:" + request.session['email'])


def get_session(request):
    print("SESJA GET:" + request.session['email'])
    return request.session['email']
