from django.conf.urls import url

from edziekanat_app.forms import *
from .views.admin import database, tools
from .views.inbox import read_messages, inbox
from .views.index import index
from .views.invoices import InvoiceCreator, manage_invoices, get_reject_info, invoice_download, invoices_list, \
    create_invoice_category, invoices
from .views.users import UserCreator, administrators, user_logout, user_login

app_name = 'edziekanat_app'

urlpatterns = [
    url(r'^$', index, name="home"),
    url(r'^login/$', user_login, name='user_login'),
    url(r'^register/$', UserCreator.as_view([RegisterForm, RegisterExtraForm]), name='user_register'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^inbox/$', inbox, name='inbox'),


    url(r'^invoices/$', invoices, name='invoices'),
    url(r'^create_invoice_category/$', create_invoice_category, name='create_invoice_category'),
    url(r'^read_messages/$', read_messages, name='read_messages'),
    url(r'^invoices_list/$', invoices_list, name='invoices_list'),
    url(r'^invoice_download/$', invoice_download, name='invoice_download'),
    url(r'^get_reject_info/$', get_reject_info, name='get_reject_info'),
    url(r'^manage_invoices/$', manage_invoices, name='manage_invoices'),
    url(r'^create_invoice/$', InvoiceCreator.as_view([InvoiceFieldPickForm, InvoiceCategoryPickForm, InvoiceFillForm]),
        name='create_invoice'),

    url(r'^administrators/$', administrators, name='administrators'),
    url(r'^tools/$', tools, name='tools'),
    url(r'^database/$', database, name='database'),
]
