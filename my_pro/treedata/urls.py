# coding: utf-8

from django.conf.urls import url
from . import views

app_name = 'treedata'

urlpatterns = [
    url(r'^process/$', views.process_list, name='process_list'),
    url(r'^process/shownodes/$', views.showNodes, name='showNodes'),
    url(r'^process/addForm/$', views.addForm, name='addForm'),
    url(r'^process/addfaliure/$', views.addFaliure, name='addfaliure'),
    url(r'^process/addData/$', views.addData, name='addData'),
]
