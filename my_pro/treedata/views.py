# coding: utf-8

from nameko.rpc import rpc
from django.http import (JsonResponse)
from django.shortcuts import (render)
from sqlalchemy.orm import joinedload

from info.database_relation import *
from info.mysql_con import OperateDatabase

from treedata.showdata.process import (jsonData, json_failure, json_control, json_process)
import json
from django.utils.http import urlquote

from treedata.showdata.pfmea import ReaPFMEA


operation_database = OperateDatabase()


def process_list(request):
    if request.method == 'GET':
        with operation_database.session_scope() as session:
            user = session.query(User).filter(User.id == request.session['id']).first()
            project = session.query(Project).filter(Project.company_id == user.company_id).first()#暂定不知选择那一个项目
            nodes = json_process(session, project.id)
            return render(request, 'treedata/process_list.html', {'nodes': nodes})

def showNodes(request):
    if request.method == 'GET':
        node_id = request.GET.get('id')
        with operation_database.session_scope() as session:
            process = session.query(Process).filter(Process.id == node_id).first()
            nodes_failure = json_failure(session, node_id)
            # nodes_control = json_control(session, node_id)
            result = {'nodes_failure': nodes_failure, 'process': process.process_name, 'process_id': process.id}
            return JsonResponse(result)


def addFaliure(request):
    if request.method == 'GET':
        with operation_database.session_scope() as session:
            node_id = request.GET.get('id')
            node_type = request.GET['type']
            node_tag = request.GET['node']
            faliure_nodes = []
            if node_tag == 'feature':
                faliures = session.query(FailureMode).filter(FailureMode.feature_id == node_id).all()
            elif node_tag == 'variation':
                faliures = session.query(FailureMode).filter(FailureMode.variation_id == node_id).all()
            elif node_tag == 'requirement':
                faliures = session.query(FailureMode).filter(FailureMode.requirement_id == node_id).all()
            for faliure in faliures:
                mode = {'id': faliure.id, 'text': faliure.failure_mode_name, 'icon': 'fa fa-chain-broken', 'color': '#FF0000'}
                faliure_nodes.append(mode)
            return render(request, 'treedata/failure_add.html', {'failure_nodes': faliure_nodes, 'node_id': node_id, 'node_tag': node_tag})
    else:
        with operation_database.session_scope() as session:
            modes = json.loads(request.body)['failure_modes']
            for mode in modes:
                failure_mode = FailureMode()
                failure_cause = FailureCauses()
                failure_effect = FailEffects()
                if mode['node_tag'] == 'feature':
                    failure_mode.feature_id = mode['node_id']
                elif mode['node_tag'] == 'variation':
                    failure_mode.variation_id = mode['node_id']
                elif mode['node_tag'] == 'requirement':
                    failure_mode.requirement_id = mode['node_id']
                failure_mode.failure_mode_name = mode['mode']
                for cause in mode['cause']:
                    failure_cause.causes_content = cause
                    failure_mode.failure_causes.append(failure_cause)
                for effect in mode['effect']:
                    failure_effect.effects_content = effect
                    failure_mode.failure_effects.append(failure_effect)
                session.add(failure_mode)
            return HttpResponse('提交成功')


def pfmea_list(request):
    with operation_database.session_scope() as session:
        nodes = PFMEA.r_json_pfmea(session)
        return JsonResponse(nodes)


def showNodes(request):
    if request.method == 'GET':
        node_id = request.GET.get('id')
        node_type = request.GET.getlist('type[]')
        with operation_database.session_scope() as session:
            nodes_failure = json_failure(session, node_type[0], node_id)
            nodes_control = json_control(session, node_type[0], node_id)
            result = {'nodes_failure': nodes_failure, 'nodes_control': nodes_control}
            return JsonResponse(result)


def addForm(request):
    if request.method == 'GET':
        process_id = request.GET.get('id')
        node_type = request.GET['type']
        node = request.GET.get('type')
        with operation_database.session_scope() as session:
            data_list = []
            process = session.query(Process).options(joinedload(Process.product_features), \
                                                     joinedload(Process.procedure_variations),
                                                     joinedload(Process.requirements)). \
                filter(Process.id == process_id).first()
            if node_type == 'product':
                fake_data = session.query(Data).filter(Data.feature == True). \
                    filter(Data.process_id == process_id).all()
                for data in fake_data:
                    user = session.query(User).filter(User.id == data.user_id).first()
                    data_li = {'id': data.id, 'username': user.username, 'text': data.fake_data}
                    data_list.append(data_li)
            elif node_type == 'requirement':
                fake_data = session.query(Data).filter(Data.requirement == True). \
                    filter(Data.process_id == process_id).all()
                for data in fake_data:
                    user = session.query(User).filter(User.id == data.user_id).first()
                    data_li = {'id': data.id, 'username': user.username, 'text': data.fake_data}
                    data_list.append(data_li)
            elif node_type == 'variation':
                fake_data = session.query(Data).filter(Data.variation == True). \
                    filter(Data.process_id == process_id).all()
                for data in fake_data:
                    user = session.query(User).filter(User.id == data.user_id).first()
                    data_li = {'id': data.id, 'username': user.username, 'text': data.fake_data}
                    data_list.append(data_li)
            feature_data = []
            variation_data = []
            requirement_data = []
            for product in process.product_features:
                feature = {'id': product.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ', \
                           'text': product.product_features}
                feature_data.append(feature)
            for procedure_variation in process.procedure_variations:
                variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B', \
                             'text': procedure_variation.procedure_variation}
                variation_data.append(variation)
            for requirement in process.requirements:
                req = {'id': requirement.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog', \
                       'text': requirement.requirement}
                requirement_data.append(req)
            print(data_list)
            return render(request, 'treedata/process_add.html', {'feature_data': feature_data, \
                                                                 'node_type': node, 'variation_data': variation_data,
                                                                 'requirement_data': requirement_data, \
                                                                 'process_id': process_id, 'fake_data': data_list})


def addData(request):
    if request.method == 'GET':
        pro_id = request.GET.get('pro_id')
        text = request.GET.get('text')
        node_type = request.GET.get('node_type')
        with operation_database.session_scope() as session:
            user = session.query(User).filter(User.id == request.session['id']).first()
            fake_data = Data()
            fake_data.user_id = user.id
            fake_data.fake_data = text
            fake_data.process_id = pro_id
            if node_type == u'product':
                fake_data.feature = True
            elif node_type == u'requirement':
                fake_data.requirement = True
            elif node_type == u'variation':
                fake_data.variation = True
            if node_type == 'product':
                fake_data.feature = True
                session.add(fake_data)
                data_list = []
                fake_data = session.query(Data).filter(Data.feature == True). \
                    filter(Data.process_id == pro_id).all()
                for data in fake_data:
                    user = session.query(User).filter(User.id == data.user_id).first()
                    result = dict(id=data.id, text=data.fake_data, username=user.username)
                    data_list.append(result)
            elif node_type == 'requirement':
                fake_data.requirement = True
                session.add(fake_data)
                data_list = []
                fake_data = session.query(Data).filter(Data.requirement == True). \
                    filter(Data.process_id == pro_id).all()
                for data in fake_data:
                    user = session.query(User).filter(User.id == data.user_id).first()
                    result = dict(id=data.id, text=data.fake_data, username=user.username)
                    data_list.append(result)
            elif node_type == 'variation':
                fake_data.variation = True
                session.add(fake_data)
                data_list = []
                fake_data = session.query(Data).filter(Data.variation == True). \
                    filter(Data.process_id == pro_id).all()
                for data in fake_data:
                    user = session.query(User).filter(User.id == data.user_id).first()
                    result = dict(id=data.id, text=data.fake_data, username=user.username)
                    data_list.append(result)
            return JsonResponse({'data': data_list})

