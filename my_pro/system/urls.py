# coding: utf-8
from django.conf.urls import url
from . import views

app_name = 'system'

urlpatterns = [
    url(r'^menu_list/$', views.menu_list, name='menu_list'),
]
