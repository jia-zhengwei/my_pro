# coding: utf-8
from django.conf.urls import url
from . import views

app_name = 'common'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^regist/$', views.toRegist, name = 'toRegist'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^group_list/$', views.group_list, name='group_list'),
    url(r'^group_add/$', views.group_add, name='group_add'),
    url(r'^group_add_user/$', views.group_add_user, name='group_add_user'),# 选择不同的组删除成员
    url(r'^lockscreen/$', views.lockscreen, name='lockscreen'),
    url(r'^login_again/$', views.login_again, name='login_again'),
    url(r'^group_user/(?P<group_id>[0-9]+)/$', views.group_user, name='group_user'),
    url(r'^del_group_user/(?P<group_id>[0-9]+)/$', views.del_group_user, name='del_group_user'),
    url(r'^add_group_user/(?P<group_id>[0-9]+)/$', views.add_group_user, name='add_group_user'),
]
