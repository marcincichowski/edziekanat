from . import views
from django.urls import path
from django.conf.urls import url

app_name = 'edziekanat_app'
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^applications/$', views.applications, name='applications'),
    url(r'^administrators/$', views.administrators, name='administrators'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^dictionaries/$', views.dictionaries, name='dictionaries')
]
