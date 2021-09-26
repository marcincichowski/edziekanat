import edziekanat_app.urls
from django.conf.urls import url
from django.urls import path

from edziekanat_app.forms import *
from . import views
from edziekanat_app.views import InvoiceCreator, UserCreator

app_name = 'edziekanat_app'

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^register/$', UserCreator.as_view([RegisterForm, RegisterExtraForm]), name='user_register'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^account/$', views.account, name='account'),
    url(r'^invoices/$', views.invoices, name='invoices'),
    url(r'^create_invoice_category/$', views.create_invoice_category, name='create_invoice_category'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^invoices_list/$', views.invoices_list, name='invoices_list'),
    url(r'^invoice_download/$', views.invoice_download, name='invoice_download'),
    url(r'^get_reject_info/$', views.get_reject_info, name='get_reject_info'),
    url(r'^manage_invoices/$', views.manage_invoices, name='manage_invoices'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^create_invoice/$', InvoiceCreator.as_view([InvoiceFieldPickForm, InvoiceCategoryPickForm, InvoiceFillForm]), name='create_invoice'),
    url(r'^administrators/$', views.administrators, name='administrators'),
    url(r'^config/$', views.config, name='config'),
    url(r'^database/$', views.database, name='database'),
]
