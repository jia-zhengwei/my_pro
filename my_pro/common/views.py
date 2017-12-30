from django.shortcuts import (render, redirect)
from django.http import (FileResponse, HttpResponse, JsonResponse)
from info.database_relation import *
from info.mysql_con import OperateDatabase
import datetime
from sqlalchemy.orm import joinedload
from common.models import *
from common.forms import RegistForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# from datetime import timedelta

operation_database = OperateDatabase()

@csrf_exempt
def user_login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login01.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(username=email, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('common:index')
        else:
            return render(request, 'login01.html')


def toRegist(request):
    """注册"""
    if request.method == 'GET':
        reg_form = RegistForm()
        return render(request, 'regist.html', {'reg_form': reg_form})
    else:
        reg_form = RegistForm(request.POST)
        print(reg_form)
        if reg_form.is_valid():
            print(reg_form.cleaned_data)
            print(reg_form.save())
        return redirect('common:login')


@login_required
def index(request):
    """进入首页"""
    if request.method == 'GET':
        return render(request, 'index.html')


def user_logout(request):
    """
    用户登出
    :param request:
    :return:
    """
    logout(request)
    return redirect('common:login')


def user_list(request):
    """用户列表"""
    user_list = []
    users = []
    with operation_database.session_scope() as session:
        user_id = request.session.get('user')['id']
        log_user = session.query(User).filter(User.id == user_id).first()
        if log_user.company_id:
            users = session.query(User).filter(User.company_id == log_user.company_id).all()
        else:
            user_list.append(log_user)
        for user in users:
            user_list.append(user)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def group_list(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        return render(request, 'user/group.html', {'groups': groups})


def lockscreen(request):
    """
        锁屏
        :param request:
        :return:
        """
    return render(request, 'user/lockscreen.html')


def login_again(request):
    """
    锁屏登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        with operation_database.session_scope() as session:
            user_id = request.session.get('id')
            user = session.query(User).filter(User.id == user_id).first()
            print(password ,'aaaaaaaaaa', user.password)
            if user.password == password:
                return render(request, 'index.html', {'username': user.username})


@login_required
def group_add(request):
    """
    添加修改分组
    """
    if request.method == 'POST':
        group_name = request.POST.get('pro_name')
        descripe = request.POST.get('pro_descripe')
        print(group_name, descripe )
        with operation_database.session_scope() as session:
            user = session.query(User).filter(User.id == request.session.get('id')).first()
            group = Group()
            group.group_name = group_name
            group.descripe =  descripe
            group.company_id = user.company_id
            session.add(group)
            #return render(request,'user/group_list.html')
            return redirect('common:group_list')
    else:
        return render(request, 'user/group_add.html')


def group_add_user(request):
    if request.method == 'POST':
        use_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        print(use_id, group_id)
        with operation_database.session_scope() as session:
            user_select = session.query(User).filter(User.id == use_id ).first()
            group_select = session.query(Group).filter(Group.id == group_id ).first()
            print(user_select, group_select)
            user_select.groups.append(group_select)
            return render(request,'user/group_list.html')

def add_group_user(request, group_id):
    if request.method == 'POST':
        user_id = request.POST.get('company_user_id')
        with operation_database.session_scope() as session:
            user_select = session.query(User).filter(User.id == user_id).first()
            group_select = session.query(Group).filter(Group.id == group_id).first()
            user_select.groups.append(group_select)
            print("qqqqqqqqqqqqq")
            print(user_select, group_select)
            return redirect('common:group_user', group_id)


def group_user(request, group_id):
    """
    进入用户组成员
    :param request:
    :return:
    """
    if request.method == 'GET':
        group_user_list = []
        with operation_database.session_scope() as session:
            user = session.query(User).filter(User.id == request.session.get('id')).first()
            group = session.query(Group).filter(Group.company_id == user.company_id)\
                .filter(Group.id == group_id).first()
            company_users = session.query(User).filter(User.company_id == user.company_id).all()
            print(group.group_name, group.users)
            return render(request, 'user/group_user.html', {'group': group, 'group_users': group.users,\
                                                            'company_users':company_users})


def del_group_user(request, group_id):
    """
    删除用户组成员
    :param request:
    :return:
    """
    if request.method == 'POST':
        del_user_id = request.POST.get('user_id')
        with operation_database.session_scope() as session:
            del_user = session.query(User).filter(User.id == del_user_id).first()
            del_group = session.query(Group).filter(Group.id == group_id).first()
            del_group.users.remove(del_user)
            return redirect('common:group_user', group_id)
