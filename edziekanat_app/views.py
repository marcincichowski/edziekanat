from django.shortcuts import render, HttpResponse
import datetime
import threading
import time

def index(request, *args, **kwargs):
    context = {
        "time": datetime.datetime.now(),
        "logged_in": False
    }
    return render(request, 'edziekanat_app/index.html', context)


def login(request, *args, **kwargs):
    context = {
        "time": datetime.datetime.now(),
        "logged_in": False
    }
    #t = threading.Thread(target=loop)
    #t.setDaemon(True)
    #t.start()
    return render(request, 'edziekanat_app/auth/login.html', context)


def register(request, *args, **kwargs):
    context = {
        "time": datetime.datetime.now(),
    }
    return render(request, 'edziekanat_app/auth/register.html', context)
