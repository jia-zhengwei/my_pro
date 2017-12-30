# coding: utf-8
"""
应用程序的urlconf
"""

from django.conf.urls import url
from . import views

app_name = 'pfmea'

urlpatterns = [
    url(r'^insert/$', views.insert_database, name='insert_database'),
    url(r'^data_import/$', views.fs_data_import, name='data_import'),
    url(r'^data_output/$', views.file_download_page, name='data_output'),
    url(r'^output_data/$', views.build_excel, name='output_data'),
    url(r'^data_update/$', views.fs_data_update, name='data_update'),
    url(r'^import_record/$', views.import_record, name='import_record'),
    url(r'^data_update/addForm/$', views.addForm, name='addForm'),
    url(r'^data_update/newData/$', views.newData, name='newData'),
    url(r'^data_update/data_list/$', views.data_list, name='data_list'),
    url(r'^data_update/treeData_add/$', views.treeData_add, name='treeData_add'),
    url(r'^data_update/treeData_update/$', views.treeData_update, name='treeData_update'),
    url(r'^data_update/treeData_del/$', views.treeData_del, name='treeData_del'),
    url(r'^data_update/treeData_create/$', views.treeData_create, name='treeData_create'),
]

