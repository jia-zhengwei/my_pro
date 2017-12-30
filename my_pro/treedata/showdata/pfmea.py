# coding: utf-8
import json

from nameko.rpc import rpc
from sqlalchemy.orm import joinedload


class ReaPFMEA(object):
	name = "relation_pfmea"

	@rpc
	def query(self):
		"""
		TODO 完善增删改功能
		:return: 关系型pfmea的json
		"""
		from info.database_relation import (Process, FailureMode, FailEffects, FailureCauses, ActionTakenResult)
		from info.mysql_con import OperateDatabase
		operation_databases = OperateDatabase()
		with operation_databases.session_scope() as session:
			pfmea_list = []
			process = session.query(Process).options(joinedload(Process.requirements)).all()
			for p in process:
				a = {'id': p.id, 'icon': 'glyphicon glyphicon-retweet', 'state': {},
				     'text': str(p.process_code) + str(p.process_name),
				     'nodes': [], 'tags': ['process']}

				for requirement in p.requirements:
					req = {"id": requirement.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
					       "text": requirement.requirement, 'tags': ['requirement']}
					a['nodes'].append(req)

					failure_modes = session.query(FailureMode).filter(
						FailureMode.requirement_id == requirement.id).all()
					for failure_mode in failure_modes:
						# 失效模式
						b = {'id': failure_mode.id, 'icon': 'fa fa-hourglass', 'color': '#00868B',
						     'text': failure_mode.failure_mode_name, 'tags': ['failure_mode'], 'nodes': []}
						# 分类
						b1 = {'id': failure_mode.id, 'icon': 'fa fa-hourglass', 'color': '#00868B',
						      'text': failure_mode.classification, 'tags': ['classification']}
						b['nodes'].append(b1)
						fail_effects = session.query(FailEffects).filter(
							FailEffects.failure_mode_id == failure_mode.id).all()

						# 潜在失效影响
						for fail_effect in fail_effects:
							c = {'id': fail_effect.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							     'text': fail_effect.effects_content, 'tags': ['fail_effect']}
							d = {'id': fail_effect.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							     'text': fail_effect.severity, 'tags': ['severity']}
							b['nodes'].append(c)
							b['nodes'].append(d)

						# 潜在失效原因
						failure_causes = session.query(FailureCauses).filter(
							FailureCauses.failure_mode == failure_mode.id).all()
						for failure_cause in failure_causes:
							e = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							     'text': failure_cause.causes_content, 'tags': ['failure_cause'], 'nodes': []}

							action_taken_results = session.query(ActionTakenResult).filter(
								ActionTakenResult.failure_causes_id == failure_cause.id).all()
							for at in action_taken_results:
								at1 = {'id': at.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
								       'text': at.severity, 'tags': ['severity']}

								at2 = {'id': at.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
								       'text': at.occurrence, 'tags': ['occurrence']}

								at3 = {'id': at.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
								       'text': at.detection, 'tags': ['detection']}

								at4 = {'id': at.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
								       'text': at.RPN, 'tags': ['RPN']}

								at5 = {'id': at.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
								       'text': at.responsibility, 'tags': ['responsibility']}

								at6 = {'id': at.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
								       'text': at.completion_date, 'tags': ['completion_date']}
								e['nodes'].append(at1)
								e['nodes'].append(at2)
								e['nodes'].append(at3)
								e['nodes'].append(at4)
								e['nodes'].append(at5)
								e['nodes'].append(at6)
							b['nodes'].append(e)

							e1 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.occurrence, 'tags': ['occurrence']}
							b['nodes'].append(e1)

							e2 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.detection, 'tags': ['detection']}
							b['nodes'].append(e2)

							e3 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.control_prevention, 'tags': ['control_prevention']}
							b['nodes'].append(e3)

							e4 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.control_detection, 'tags': ['control_detection']}
							b['nodes'].append(e4)

							e5 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.RPN, 'tags': ['RPN']}
							b['nodes'].append(e5)

							e6 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.recommended_action, 'tags': ['recommended_action']}
							b['nodes'].append(e6)

							e7 = {'id': failure_cause.id, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
							      'text': failure_cause.responsibility_completion_date,
							      'tags': ['responsibility_completion_date']}
							b['nodes'].append(e7)
						a['nodes'].append(b)
				pfmea_list.append(a)
			return pfmea_list

	@rpc
	def insert(self, update_json):
		from info.mysql_con import OperateDatabase
		update_data = json.load(update_json)
		with OperateDatabase.session_scope as session:
			pass
		pass

	@rpc
	def delete(self, update_json):
		# 删除行的操作 **不是单个Column**
		delete_data = json.load(update_json)
		from info.database_relation import (Process, ProcessFlow, Requirement, FailureMode, FailEffects, FailureCauses,
		                                    InputVariation, ProcedureVariation,
		                                    ActionTakenResult, ControlPlan)
		from info.mysql_con import OperateDatabase
		with OperateDatabase.session_scope as session:
			if delete_data['tags'] == 'Process':
				# 删除相关的Process时同时删除相对应的所有关联的
				# 这里使用first是只有一个数据没有重复
				d = session.query(Process).filter(Process.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'ProcessFlow':
				d = session.query(ProcessFlow).filter(ProcessFlow.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'Requirement':
				d = session.query(Requirement).filter(Requirement.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'FailureMode':
				d = session.query(FailureMode).filter(FailureMode.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'FailEffects':
				d = session.query(FailEffects).filter(FailureMode.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'FailureCauses':
				d = session.query(FailureCauses).filter(FailureCauses.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'InputVariation':
				d = session.query(InputVariation).filter(InputVariation.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'ProcedureVariation':
				d = session.query(ProcedureVariation).filter(ProcedureVariation.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'ActionTakenResult':
				d = session.query(ActionTakenResult).filter(ActionTakenResult.id == delete_data['id']).first()
				session.delete(d)
			elif delete_data['tags'] == 'ControlPlan':
				d = session.query(ControlPlan).filter(ControlPlan.id == delete_data['id']).first()
				session.delete(d)

	@rpc
	def alter(self, update_json):
		update_data = json.load(update_json)
		from info.database_relation import (Process, ProcessFlow, Requirement, FailureMode, FailEffects,
		                                    FailureCauses, )
		from info.mysql_con import OperateDatabase
		with OperateDatabase.session_scope as session:
			if update_data['tags'] == 'Process':
				process = session.query(Process).filter_by(id == update_data['id']).scalar()
				process.process_name = update_data['process_name']
				process.process_code = update_data['process_code']
			elif update_data['tags'] == 'ProcessFlow':
				# 这里添加了database_relation ProcessFlow中的flow json字段
				flow = session.query(ProcessFlow).filter_by(id == update_data['id']).scalar()
				flow.flow = update_data['text']
			elif update_data['tags'] == 'requirement':
				reqs = session.query(Requirement).filter_by(id == update_data['id']).scalar()
				reqs.requirement = update_data['text']
			elif update_data['tags'] == 'failure_mode':
				fm = session.query(FailureMode).filter_by(id == update_data['id']).scalar()
				fm.failure_mode_name = update_data['text']
			elif update_data['tags'] == 'classification':
				fm = session.query(FailureMode).filter_by(id == update_data['id']).scalar()
				fm.failure_mode_name = update_data['text']
			elif update_data['tags'] == 'rpn':
				fm = session.query(FailureMode).filter_by(id == update_data['id']).scalar()
				fm.failure_mode_name = update_data['text']
			elif update_data['tags'] == 'fail_effect':
				fe = session.query(FailEffects).filter_by(id == update_data['id']).scalar()
				fe.effects_content = update_data['text']
			elif update_data['tags'] == 'severity':
				fe = session.query(FailEffects).filter_by(id == update_data['id']).scalar()
				fe.severity = update_data['text']
			elif update_data['tags'] == 'failure_cause':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.causes_content = update_data['text']
			elif update_data['tags'] == 'occurrence':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.occurrence = update_data['text']
			elif update_data['tags'] == 'detection':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.detection = update_data['text']
			elif update_data['tags'] == 'control_prevention':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.control_prevention = update_data['text']
			elif update_data['tags'] == 'control_detection':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.control_detection = update_data['text']
			elif update_data['tags'] == 'RPN':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.RPN = update_data['text']
			elif update_data['tags'] == 'recommended_action':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.recommended_action = update_data['text']
			elif update_data['tags'] == 'responsibility_completion_date':
				fc = session.query(FailureCauses).filter_by(id == update_data['id']).scalar()
				fc.responsibility_completion_date = update_data['text']


class JsPFMEA(object):
	name = 'json_pfmea'

	@rpc
	def query(self):
		"""
		:return: JSON字段的pfmea json
		"""
		from dbctrl.mysql_con import OperateDatabase
		from dbctrl.db_relation import (Process, PFMEA)
		with OperateDatabase.session_scope() as session:
			pfmea_list = []
			processes = session.query(Process).all()
			for process in processes:
				p = {'id': process.id, 'icon': 'glyphicon glyphicon-retweet', 'state': {},
				     'text': str(process.process_code) + str(process.process_name),
				     'nodes': [], 'tags': ['process']}
				json_pfmeas = session.query(PFMEA).filter(PFMEA.process_id == process.id).all()

				for pfmea in json_pfmeas:
					fme = json.load(pfmea)
					# 在fmea json中不存在ID
					for res in fme.keys:
						req = {'text': res, 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
						       'tags': ['requirement'], 'nodes': []}

						# 失效模式
						for fm in fme[res]:
							fme = {'text': fm.key, 'icon': 'fa fa-hourglass', 'color': '#00868B',
							       'tags': ['failure_mode'], 'nodes': [
									{'text': fm['effects_content'], 'color': '#00EE76',
									 'icon': 'glyphicon glyphicon-cog',
									 'tags': ['effects_content']},
									{'text': fm['severity'], 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
									 'tags': ['severity']},
									{'text': fm['classification', 'color': '#00EE76', 'icon': 'glyphicon glyphicon-cog',
									         'tags': ['classification']]}
								]}

							# 失效原因
							for fc in fm[fm.key]:
								ffc = {'text': fc.key, 'icon': 'fa fa-hourglass', 'color': '#00868B',
								       'tags': ['failure_causes'], 'nodes': [
										{'text': fc['occurrence'], 'icon': 'fa fa-hourglass', 'color': '#00868B',
										 'tags': ['occurrence']},
										{'text': fc['detection'], 'icon': 'fa fa-hourglass', 'color': '#00868B',
										 'tags': ['detection']},
										{'text': fc['control_prevention'], 'icon': 'fa fa-hourglass',
										 'color': '#00868B',
										 'tags': ['control_prevention']},
										{'text': fc['control_detection'], 'icon': 'fa fa-hourglass', 'color': '#00868B',
										 'tags': ['control_detection']},
										{'text': fc['RPN'], 'icon': 'fa fa-hourglass', 'color': '#00868B',
										 'tags': ['RPN']},
										{'text': fc['recommended_action'], 'icon': 'fa fa-hourglass',
										 'color': '#00868B',
										 'tags': ['recommended_action']},
										{'text': '执行结果', 'icon': 'fa fa-hourglass', 'color': '#00868B',
										 'tags': ['action_taken_result'], 'nodes': [
											{'text': fc['action_taken_result']['severity'], 'icon': 'fa fa-hourglass',
											 'color': '#00868B',
											 'tags': ['action_taken_result']},
											{'text': fc['action_taken_result']['occurrence'], 'icon': 'fa fa-hourglass',
											 'color': '#00868B', 'tags': ['occurrence']},
											{'text': fc['action_taken_result']['detection'], 'icon': 'fa fa-hourglass',
											 'color': '#00868B', 'tags': ['detection']},
											{'text': fc['action_taken_result']['RPN'], 'icon': 'fa fa-hourglass',
											 'color': '#00868B', 'tags': ['RPN']},
											{'text': fc['action_taken_result']['responsibility'],
											 'icon': 'fa fa-hourglass',
											 'color': '#00868B',
											 'tags': ['responsibility']},
											{'text': fc['action_taken_result']['completion_date'],
											 'icon': 'fa fa-hourglass',
											 'color': '#00868B',
											 'tags': ['completion_date']},

										]}
									]}
								fme['nodes'].append(ffc)
							req['nodes'].append(fme)
					p['nodes'].append(req)
				pfmea_list.append(p)
			return pfmea_list

	@rpc
	def alter(self, insert_json):
		"""
		:param insert_json: 修改之后的一行字段
		:return:
		"""
		from dbctrl.mysql_con import OperateDatabase
		from dbctrl.db_relation import Process, PFMEA
		insert_data = json.load(insert_json)
		with OperateDatabase.session_scope() as session:
			if insert_data['tags'] == 'process':
				# 这里是修改过程名称
				alt = session.query(Process).filter(Process.id == insert_data['id']).first()
				alt.process_name = insert_data['text']
			else:
				alt = session.query(PFMEA).filter(PFMEA.id == insert_data['id']).first()
				alt.pfmea = insert_data['json']

	@rpc
	def delete(self, target_json):
		# 该功能是删除整行的PFMEA数据
		from dbctrl.mysql_con import OperateDatabase
		from dbctrl.db_relation import PFMEA
		insert_data = json.load(target_json)
		with OperateDatabase.session_scope() as session:
			d = session.query(PFMEA).filter(PFMEA.id == insert_data['id']).first()
			session.delete(d)


if __name__ == '__main__':
	# with operation_databases.session_scope() as session:
	# 	print(json_pfmea(session))
	print(ReaPFMEA().query())
