from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import RegisterForm, LoginForm
import datetime
import threading
import time


def index(request, *args, **kwargs):
    context = {
        "time": datetime.datetime.now(),
        "logged_in": False
    }
    return render(request, 'edziekanat_app/index.html', context)



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

                return render(request, 'edziekanat_app/index.html')
            else:
                return render(request, 'edziekanat_app/user/login.html',{
                    'form': form,
                    "time": datetime.datetime.now(),
                    'error_message': 'Wprowadzono niepoprawne dane.'
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form})


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

                return HttpResponseRedirect('index.html')

    else:
        form = RegisterForm()

    return render(request, template, {'form': form})
