from . import views
from django.urls import path
from django.conf.urls import url

app_name = 'edziekanat_app'
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^register/$', views.user_register, name='user_register')
]
