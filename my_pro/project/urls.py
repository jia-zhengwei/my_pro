# coding: utf-8

from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [
    url(r'^list/$', views.project_list, name='project_list'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^edit_project(?P<pro_id>[0-9]+)/$', views.edit_project, name='edit_project'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^get_document/$', views.get_document, name='get_document'),
    url(r'^del_project(?P<pro_id>[0-9]+)/$', views.del_project, name='del_project'),
    # url(r'^(?P<doc_id>[0-9]+)/$', views.download_file, name='download_file'),
]
