# coding: utf-8

from sqlalchemy.orm import joinedload

from info.database_relation import *
from info.mysql_con import OperateDatabase

operation_databases = OperateDatabase()


def json_nodes(nodes, failure_modes):
    """
    返回失效模式的数据
    """
    for failure_mode in failure_modes:
        mode = {'id': failure_mode.id, 'text': failure_mode.failure_mode_name, \
        'icon': 'fa fa-chain-broken', 'tags': ['mode'], 'color': '#FF0000', 'nodes':[]}
        for failure_cause in failure_mode.failure_causes:
            cause = {'id': failure_cause.id, 'text': failure_cause.causes_content, \
            'icon': 'fa fa-link', 'tags': ['cause'], 'nodes': []}
            param = {'text': 'D='+str(failure_cause.detection)+' '+'O='+str(failure_cause.occurrence)+' '+ \
            'RPN='+ str(failure_cause.RPN)}
            cause['nodes'].append(param)
            mode['nodes'].append(cause)
        for failure_effect in failure_mode.failure_effects:
            effect = {'id': failure_effect.id, 'text': failure_effect.effects_content, \
            'icon': 'fa fa-houzz', 'tags': ['effect'], 'nodes': []}
            mode['nodes'].append(effect)
        nodes['nodes'].append(mode)
    return nodes


def jsonData(session):
    """
    返回过程要求，失效模式，工艺特性，产品特性
    :return:返回treeview所需要的是数据格式
    """
    processes = session.query(Process).options(joinedload(Process.requirements)).all()
    nodes = []
    for process in processes:
        pro = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'text': str(process.process_code)+str(process.process_name), \
            'nodes': [], 'tags': ['process']}
        product_features = session.query(ProductFeature).filter(ProductFeature. \
            process_id == process.id).filter(ProductFeature.excel_control == True).all()
        procedure_variations = session.query(ProcedureVariation).filter(ProcedureVariation. \
            process_id == process.id).filter(ProcedureVariation.excel_control == True).all()
        for product_feature in product_features:
            feature = {'id': product_feature.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ', \
            'text': product_feature.product_features, 'tags': ['feature']}
            pro['nodes'].append(feature)
        for procedure_variation in procedure_variations:
            variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B', \
            'text': procedure_variation.procedure_variation, 'tags': ['variation']}
            pro['nodes'].append(variation)
        for requirement in process.requirements:
            req = {'id': requirement.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog', 'text': requirement.requirement, 'tags': ['requirement']}
            pro['nodes'].append(req)
        nodes.append(pro)
    return nodes


def json_failure(session, identity):
    """
    param:{session: 数据库session会话，type:要查询的数据类型，identity:数据的id}
    return:返回数据nodes，失效模式，控制计划，预防措施
    """
    nodes = []
    process = session.query(Process).options(joinedload(Process.requirements)).\
        filter(Process.id == identity).first()
    # pro = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'state':{'expanded': 'false'}, \
    # 'text': str(process.process_name), \
    #     'tags': ['process'], 'nodes': []}
    product_features = session.query(ProductFeature).filter(ProductFeature. \
        process_id == process.id).filter(ProductFeature.excel_control == True).all()
    procedure_variations = session.query(ProcedureVariation).filter(ProcedureVariation. \
        process_id == process.id).filter(ProcedureVariation.excel_control == True).all()
    for product_feature in product_features:
        feature = {'id': product_feature.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ', \
        'text': product_feature.product_features, 'tags': ['feature'], 'nodes': []}
        failure_modes = session.query(FailureMode).options(joinedload(FailureMode.failure_causes), \
            joinedload(FailureMode.failure_effects)).filter(FailureMode.feature_id == product_feature.id).all()
        feature_nodes = json_nodes(feature, failure_modes)
        nodes.append(feature_nodes)
    for procedure_variation in procedure_variations:
        variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B', \
        'text': procedure_variation.procedure_variation, 'tags': ['variation'], 'nodes': []}
        failure_modes = session.query(FailureMode).options(joinedload(FailureMode.failure_causes), \
            joinedload(FailureMode.failure_effects)).filter(FailureMode.variation_id == procedure_variation.id).all()
        variation_nodes = json_nodes(variation, failure_modes)
        nodes.append(variation_nodes)
    for requirement in process.requirements:
        req = {'id': requirement.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog', \
        'text': requirement.requirement, 'tags': ['requirement'], 'nodes': []}
        failure_modes = session.query(FailureMode).options(joinedload(FailureMode.failure_causes), \
            joinedload(FailureMode.failure_effects)).filter(FailureMode.requirement_id == requirement.id).all()
        req_nodes = json_nodes(req, failure_modes)
        nodes.append(req_nodes)
    return nodes


def json_control(session, type, identity):
    """
    param:{session: 数据库session会话，type:要查询的数据类型，identity:数据的id}
    return:返回数据nodes，失效模式，控制计划，预防措施
    """
    nodes = []
    if type == 'process':
        process = session.query(Process).options(joinedload(Process.requirements)).\
            filter(Process.id == identity).first()
        pro = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'text': str(process.process_name), \
            'tags': ['process'], 'nodes': []}
        product_features = session.query(ProductFeature).options(joinedload(ProductFeature.control_plans)). \
        filter(ProductFeature.process_id == process.id).filter(ProductFeature.excel_control == True).all()
        procedure_variations = session.query(ProcedureVariation).options(joinedload(ProcedureVariation.control_plans)). \
        filter(ProcedureVariation.process_id == process.id).filter(ProcedureVariation.excel_control == True).all()
        for product_feature in product_features:
            feature = {'id': product_feature.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ', \
            'text': product_feature.product_features, 'nodes': []}
            for control_plan in product_feature.control_plans:
                plan = {'id': control_plan.id, 'text': '测量技术：'+str(control_plan.evaluation_technique)+' '+ \
                '抽样大小：'+ str(control_plan.size)+'  '+'频率：'+str(control_plan.freq)+'  '+'控制方法：'+str(control_plan.control_methods), \
                'icon': 'fa fa-joomla'}
                feature['nodes'].append(plan)
            pro['nodes'].append(feature)
        for procedure_variation in procedure_variations:
            variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B', \
            'text': procedure_variation.procedure_variation, 'nodes': []}
            for control_plan in procedure_variation.control_plans:
                plan = {'id': control_plan.id, 'text': '测量技术：'+str(control_plan.evaluation_technique)+' '+ \
                '抽样大小：'+ str(control_plan.size)+'  '+'频率：'+str(control_plan.freq)+'  '+'控制方法：'+str(control_plan.control_methods), \
                'icon': 'fa fa-joomla'}
                variation['nodes'].append(plan)
            pro['nodes'].append(variation)
        nodes.append(pro)
        return nodes


def json_process(session, project_id):
# def jsonData(session):
    """
    返回过程要求，失效模式，工艺特性，产品特性
    :return:返回treeview所需要的是数据格式
    """
    processes = session.query(Process).options(joinedload(Process.requirements)).all()
    nodes = []
    for process in processes:
        pro = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'state': {},
               'text': str(process.process_code) + str(process.process_name),
               'nodes': [], 'tags': ['process']}
        product_features = session.query(ProductFeature).filter(ProductFeature. \
                                                                process_id == process.id).filter(
            ProductFeature.excel_control == True).all()
        procedure_variations = session.query(ProcedureVariation).filter(ProcedureVariation. \
                                                                        process_id == process.id).filter(
            ProcedureVariation.excel_control == True).all()
        for product_feature in product_features:
            feature = {'id': product_feature.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ', \
                       'text': product_feature.product_features, 'tags': ['feature']}
            pro['nodes'].append(feature)
        for procedure_variation in procedure_variations:
            variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B',
                         'text': procedure_variation.procedure_variation, 'tags': ['variation']}
            pro['nodes'].append(variation)
        for requirement in process.requirements:
            req = {'id': requirement.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
                   'text': requirement.requirement, 'tags': ['requirement']}
            pro['nodes'].append(req)
        nodes.append(pro)
    return nodes


def json_failure(session, type, identity):
    """
    param:{session: 数据库session会话，type:要查询的数据类型，identity:数据的id}
    return:返回数据nodes，失效模式，控制计划，预防措施
    """
    nodes = []
    if type == 'process':
        process = session.query(Process).options(joinedload(Process.requirements)). \
            filter(Process.id == identity).first()
        pro = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'text': str(process.process_name), \
               'nodes': []}
        product_features = session.query(ProductFeature).filter(ProductFeature. \
                                                                process_id == process.id).filter(
            ProductFeature.excel_control == True).all()
        procedure_variations = session.query(ProcedureVariation).filter(ProcedureVariation. \
                                                                        process_id == process.id).filter(
            ProcedureVariation.excel_control == True).all()
        for product_feature in product_features:
            feature = {'id': product_feature.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ', \
                       'text': product_feature.product_features, 'nodes': []}
            failure_modes = session.query(FailureMode).options(joinedload(FailureMode.failure_causes), \
                                                               joinedload(FailureMode.failure_effects)).filter(
                FailureMode.feature_id == product_feature.id).all()
            feature_nodes = json_nodes(feature, failure_modes)
            pro['nodes'].append(feature_nodes)
        for procedure_variation in procedure_variations:
            variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B', \
                         'text': procedure_variation.procedure_variation, 'nodes': []}
            failure_modes = session.query(FailureMode).options(joinedload(FailureMode.failure_causes), \
                                                               joinedload(FailureMode.failure_effects)).filter(
                FailureMode.variation_id == procedure_variation.id).all()
            variation_nodes = json_nodes(variation, failure_modes)
            pro['nodes'].append(variation_nodes)
        for requirement in process.requirements:
            req = {'id': requirement.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog', \
                   'text': requirement.requirement, 'nodes': []}
            failure_modes = session.query(FailureMode).options(joinedload(FailureMode.failure_causes), \
                                                               joinedload(FailureMode.failure_effects)).filter(
                FailureMode.requirement_id == requirement.id).all()
            req_nodes = json_nodes(req, failure_modes)
            pro['nodes'].append(req_nodes)
        nodes.append(pro)
        return nodes


def json_control(session, type, identity):
    """
    param:{session: 数据库session会话，type:要查询的数据类型，identity:数据的id}
    return:返回数据nodes，失效模式，控制计划，预防措施
    """
    nodes = []
    if type == 'process':
        process = session.query(Process).options(joinedload(Process.requirements)). \
            filter(Process.id == identity).first()
        pro = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'text': str(process.process_name),
               'nodes': []}
        product_features = session.query(ProductFeature).options(joinedload(ProductFeature.control_plans)). \
            filter(ProductFeature.process_id == process.id).filter(ProductFeature.excel_control == True).all()
        procedure_variations = session.query(ProcedureVariation).options(joinedload(ProcedureVariation.control_plans)). \
            filter(ProcedureVariation.process_id == process.id).filter(ProcedureVariation.excel_control == True).all()
        for product_feature in product_features:
            feature = {'id': product_feature.id, 'icon': 'fa fa-hourglass-start', 'color': '#483D8B ',
                       'text': product_feature.product_features, 'nodes': []}
            for control_plan in product_feature.control_plans:
                plan = {'id': control_plan.id, 'text': '测量技术：' + str(control_plan.evaluation_technique) + ' ' +
                                                       '抽样大小：' + str(control_plan.size) + '  ' + '频率：' + str(
                    control_plan.freq) + '  ' + '控制方法：' + str(control_plan.control_methods),
                        'icon': 'fa fa-joomla'}
                feature['nodes'].append(plan)
            pro['nodes'].append(feature)
        for procedure_variation in procedure_variations:
            variation = {'id': procedure_variation.id, 'icon': 'fa fa-hourglass', 'color': '#00868B',
                         'text': procedure_variation.procedure_variation, 'nodes': []}
            for control_plan in procedure_variation.control_plans:
                plan = {'id': control_plan.id, 'text': '测量技术：' + str(control_plan.evaluation_technique) + ' ' +
                                                       '抽样大小：' + str(control_plan.size) + '  ' + '频率：' + str(
                    control_plan.freq) + '  ' + '控制方法：' + str(control_plan.control_methods),
                        'icon': 'fa fa-joomla'}
                variation['nodes'].append(plan)
            pro['nodes'].append(variation)
        nodes.append(pro)
        print(nodes)
        return nodes


def json_process(session, project_id):
    node = [{'key': 'index', 'text': '流程'}, \
    {'key': 'procezo', 'text': '加工', 'parent': 'index'}, \
    {'key': 'move', 'text': '搬运', 'parent': 'index'}, \
    {'key': 'storage', 'text': '储存', 'parent': 'index'}, \
    {'key': 'inspect', 'text': '检查', 'parent': 'index'}]
    processes = session.query(Process).filter(Process.project_id == project_id).all()
    for process in processes:
        process_flow = session.query(ProcessFlow).filter(process.process_flow_id == ProcessFlow.id).first()
        if process_flow.procezo != None:
            node.append(dict(key=process.id, text=process.process_name, parent='procezo'))
        elif process_flow.move != None:
            node.append(dict(key=process.id, text=process.process_name, parent='move'))
        elif process_flow.storage != None:
            node.append(dict(key=process.id, text=process, parant='storage'))
        elif process_flow.inspect != None:
            node.append(dict(key=process.id, text=process.process_name, parent='inspect'))
    return node
