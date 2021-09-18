from django.conf.urls import url

from . import views

app_name = 'edziekanat_app'
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^account/$', views.account, name='account'),
    url(r'^invoices/$', views.invoices, name='invoices'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^create_invoice/$', views.create_invoice, name='create_invoice'),
    url(r'^administrators/$', views.administrators, name='administrators'),
    url(r'^config/$', views.config, name='config'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^dictionaries/$', views.dictionaries, name='dictionaries')
]
