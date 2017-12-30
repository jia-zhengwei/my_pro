from django.shortcuts import (render, redirect)
from django.http import (FileResponse, HttpResponse, JsonResponse)
from info.database_relation import *
from info.mysql_con import OperateDatabase
import datetime
from sqlalchemy.orm import joinedload
# from datetime import timedelta

operation_database = OperateDatabase()


def menu_list(request):
    if request.method == 'GET':
        with operation_database.session_scope() as session:
            groups = session.query(Group).filter(Group.company_id == request.session['user']['company_id']).all()
            menus = session.query(Menu).all()
            return render(request, 'system/menu_group.html', {'groups': groups, 'menus': menus})
