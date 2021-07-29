from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
]
