# coding: utf-8

from database_relation import *
from mysql_con import OperateDatabase

operation_databases = OperateDatabase()


def json_process():
	with operation_databases.session_scope() as session:
		processes = session.query(Process).all()
		process_list = []
		for process in processes:
			a = {"text": str(process.process_code +
			                 process.process_name), "nodes": []}
			process_flow = session.query(ProcessFlow).filter(
				ProcessFlow.id == process.id).all()
			for i in process_flow:
				b = {"text": "过程流程", "tags": [
					str(len(process_flow))], "nodes": []}
				if i.procezo:
					b["nodes"].append(dict(text=i.procezo))
				if i.move:
					b["nodes"].append(dict(text=i.move))
				if i.storage:
					b["nodes"].append(dict(text=i.storage))
				if i.inspect:
					b["nodes"].append(dict(text=i.inspect))
				a["nodes"].append(b)

			input_variation = session.query(InputVariation).filter(
				InputVariation.process_id == process.id).all()
			for i in input_variation:
				c = {"text": "输入变差", "nodes": []}
				c["nodes"].append(dict(n=i.input_variation))
				a["nodes"].append(c)

			product_features = session.query(ProductFeature).filter(
				ProductFeature.process_id == process.id).all()

			d = {"text": "产品特性", "tags": [
				str(len(product_features))], "nodes": []}
			for i in product_features:
				d["nodes"].append(dict(id=i.id, text=i.product_features))
			a["nodes"].append(d)
			procedure_variation = session.query(ProcedureVariation).filter(
				ProcedureVariation.process_id == process.id).all()
			e = {"text": "工艺特性", "tags": [
				str(len(procedure_variation))], "nodes": []}
			for i in procedure_variation:
				e["nodes"].append(dict(id=i.id, text=i.procedure_variation))
			a["nodes"].append(e)
			process_list.append(a)

		return process_list


def json_control():
	"""
	控制计划 json
	:return:
	"""
	with operation_databases.session_scope() as session:
		processes = session.query(Process).all()
		control_list = []
		for process in processes:
			a = {'text': str(process.process_code), 'nodes': []}
			b = {'text': process.process_name, 'nodes': []}
			a['nodes'].append(b)

			# 设备工装读取出来的是列表 其中的值相同
			machines = session.query(Machine).filter(
				Machine.process_id == process.id).all()
			for machine in machines:
				c = {'text': '设备·工装', 'nodes': []}
				c['nodes'].append(dict(text=machine.machine_name, nodes=[]))
				a['nodes'].append(c)
				break

			# 工艺特性 product_feature 是否是工艺特性 在控制计划中 0为不在 1为在
			c = {'text': '特性', 'nodes': []}
			product_features = session.query(ProductFeature).filter(ProductFeature.process_id == process.id,
			                                                        ProductFeature.excel_control == 1).all()
			for product_feature in product_features:
				control_plans = session.query(ControlPlan).filter(
					ControlPlan.product_feature_id == product_feature.id).first()
				d = {'text': '方法', 'nodes': [
					dict(text=product_feature.product_features, nodes=[]), ]}
				ps = {'text': '工艺', 'nodes': []}
				d1 = {'text': '产品/过程规范',
				      'nodes': [dict(text=product_feature.tolerance, nodes=[]), ]}
				d2 = {'text': '评估/测量技术',
				      'nodes': [dict(text=control_plans.evaluation_technique, nodes=[]), ]}
				d3 = {'text': '抽样大小', 'nodes': [
					dict(text=control_plans.size, nodes=[]), ]}
				d4 = {'text': '频率', 'nodes': [
					dict(text=control_plans.freq, nodes=[]), ]}
				d5 = {'text': '控制方法', 'nodes': [
					dict(text=control_plans.control_methods, nodes=[]), ]}
				d6 = {'text': '反应计划', 'nodes': [
					dict(text=control_plans.reaction_plan, nodes=[]), ]}
				d['nodes'].append(d1)
				d['nodes'].append(d2)
				d['nodes'].append(d3)
				d['nodes'].append(d4)
				d['nodes'].append(d5)
				d['nodes'].append(d6)
				ps['nodes'].append(d)
				c['nodes'].append(ps)

			# 产品特性
			procedure_variations = session.query(ProcedureVariation).filter(ProcedureVariation.process_id == process.id,
			                                                                ProcedureVariation.excel_control == 1).all()
			for procedure_variation in procedure_variations:
				pv = {'text': '产品', 'nodes': []}
				pv['nodes'].append(
					dict(text=procedure_variation.procedure_variation, nodes=[]))
				control_plans = session.query(ControlPlan).filter(
					ControlPlan.procedure_feature_id == procedure_variation.id).first()
				d = {'text': '方法', 'nodes': [
					dict(text=procedure_variation.procedure_variation, nodes=[]), ]}
				d1 = {'text': '产品/过程规范',
				      'nodes': [dict(text=procedure_variation.tolerance, nodes=[]), ]}
				d2 = {'text': '评估/测量技术',
				      'nodes': [dict(text=control_plans.evaluation_technique, nodes=[]), ]}
				d3 = {'text': '抽样大小', 'nodes': [
					dict(text=control_plans.size, nodes=[]), ]}
				d4 = {'text': '频率', 'nodes': [
					dict(text=control_plans.freq, nodes=[]), ]}
				d5 = {'text': '控制方法', 'nodes': [
					dict(text=control_plans.control_methods, nodes=[]), ]}
				d6 = {'text': '反应计划', 'nodes': [
					dict(text=control_plans.reaction_plan, nodes=[]), ]}
				d['nodes'].append(d1)
				d['nodes'].append(d2)
				d['nodes'].append(d3)
				d['nodes'].append(d4)
				d['nodes'].append(d5)
				d['nodes'].append(d6)
				pv['nodes'].append(d)
				c['nodes'].append(pv)

			a['nodes'].append(c)
			control_list.append(a)
		return control_list


def json_pfmea():
	with operation_databases.session_scope() as session:
		processes = session.query(Process).all()
		pfmea_list = []
		for process in processes:
			a = {'text': str(process.process_code), 'nodes': []}
			requirements = session.query(Requirement).filter(
				Requirement.process_id == process.id).all()
			b = {'text': '要求', 'tags': [str(len(requirements)), str(
				process.process_name)], 'nodes': []}
			for requirement in requirements:
				req = {'id': requirement.id,
				       'text': requirement.requirement, 'nodes': []}

				b['nodes'].append(req)
				failure_modes = session.query(FailureMode).filter(
					FailureMode.requirement_id == requirement.id).all()
				c = {'text': '失效模式', 'tags': [
					str(len(failure_modes))], 'nodes': []}
				for failure_mode in failure_modes:
					mode = {'id': failure_mode.id,
					        'text': failure_mode.failure_mode_name, 'nodes': []}
					c['nodes'].append(mode)
					fail_effects = session.query(FailEffects).filter(
						FailEffects.failure_mode_id == failure_mode.id).all()
					d = {'text': '失效影响', 'tags': [
						str(len(fail_effects))], 'nodes': []}
					for fail_effect in fail_effects:
						d['nodes'].append(
							dict(id=fail_effect.id, text=fail_effect.effects_content))

					failure_causes = session.query(FailureCauses).filter(
						FailureCauses.failure_mode == failure_mode.id).all()
					e = {'text': '失效原因', 'tags': [
						str(len(failure_causes))], 'nodes': []}
					for failure_cause in failure_causes:
						e['nodes'].append(
							dict(id=failure_cause.id, text=failure_cause.causes_content))
					mode['nodes'].append(d)
					mode['nodes'].append(e)
				req['nodes'].append(c)
			a['nodes'].append(b)
			pfmea_list.append(a)
	return pfmea_list



def json_special():
	"""
	特殊清单 json
	:return:
	"""
	with operation_databases.session_scope() as session:
		processes = session.query(Process).all()
		sp_list = []
		for process in processes:
			procedure_variations = session.query(ProcedureVariation).filter(
				ProcedureVariation.special_symbol.isnot(None),
				ProcedureVariation.process_id == process.id).all()
			a = {'text': process.process_code, 'nodes': []}
			b = {'text': process.process_name, 'nodes': []}
			c = {'text': '过程特殊特性', 'nodes': []}
			for i in procedure_variations:
				d = {'text': i.procedure_variation, 'nodes': [
					{'text': '特殊特性符号', 'nodes': [
						dict(text=i.special_symbol, nodes=[]), ]},
					{'text': '法规符合性', 'nodes': [
						dict(text=i.regulatory_compliance, nodes=[]), ]},
					{'text': '安全性', 'nodes': [
						dict(text=i.safety, nodes=[]), ]},
					{'text': '功能/性能',
					 'nodes': [dict(text=i.func, nodes=[]), ]},
					{'text': '后续过程', 'nodes': [
						dict(text=i.follow_process, nodes=[]), ]},
				]}
				c['nodes'].append(d)
			sp_list.append(a)
			sp_list.append(b)
			sp_list.append(c)
		return sp_list


if __name__ == '__main__':
	json_pfmea()
