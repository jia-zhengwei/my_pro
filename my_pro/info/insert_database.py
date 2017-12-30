# coding: utf-8

from .database_relation import *
from .mysql_con import OperateDatabase

operation_database = OperateDatabase()


def insert_process(data):
	""""
	插入过程流程数据到数据库
	:return:
	"""
	process_list = []
	for j in data:
		num = len(data[j]['procedure_variation'])
		var_num = pro_num = proce_num = 1
		product_feature = ProductFeature()
		process = Process()
		process.process_code = j
		process.process_name = data[j]['procedure_name']
		while num > 0:
			for i in data[j]:
				if i == 'input_variation' and var_num < len(data[j][i]) + 1:
					for k in range(var_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							input_variation = InputVariation()
							input_variation.input_variation = data[j][i][str(k)]
							process.input_variations.append(input_variation)
							var_num += 1
							break
						else:
							var_num += 1
							break
				if i == 'product_features' and pro_num < len(data[j][i]) + 1:
					for k in range(pro_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							product_feature = ProductFeature()
							product_feature.product_features = data[j][i][str(k)]
							process.product_features.append(product_feature)
							pro_num += 1
							break
						else:
							pro_num += 1
							break
				if i == 'procedure_variation' and proce_num < len(data[j][i]) + 1:
					for k in range(proce_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							procedure_variation = ProcedureVariation()
							procedure_variation.procedure_variation = data[j][i][str(k)]
							process.procedure_variations.append(procedure_variation)
							if product_feature.product_features:
								product_feature.procedure_variations.append(procedure_variation)
							proce_num += 1
							break
						else:
							proce_num += 1
							break
			num -= 1
		for k in data[j]['procedure_spec']:
			process_flow = ProcessFlow()
			if data[j]['procedure_spec'][k] and k == 'manualfacture':
				process_flow.procezo = data[j]['procedure_spec'][k]
				process_flow.processes.append(process)
			if data[j]['procedure_spec'][k] and k == 'move':
				process_flow.move = data[j]['procedure_spec'][k]
				process_flow.processes.append(process)
			if data[j]['procedure_spec'][k] and k == 'storage':
				process_flow.storage = data[j]['procedure_spec'][k]
				process_flow.processes.append(process)
			if data[j]['procedure_spec'][k] and k == 'inspect':
				process_flow.inspect = data[j]['procedure_spec'][k]
				process_flow.processes.append(process)
		process_list.append(process)
	return process_list


def insert_pfmea(session, data):
	"""
	插入pfmea数据到数据库
	:return:
	"""
	for j in data:
		process = session.query(Process).filter(Process.process_code.like('%s' % j[0:8])).first()
		num = len(data[j]['potential_failure_causes'])
		req_num = mod_num = effect_num = sev_num = cla_num = res_num = rec_num = rpn_num = det_num = occ_num = con_num = cause_num = con_det_num = 1
		requirement = Requirement()
		failure_mode = FailureMode()
		failure_causes = FailureCauses()
		while num > 0:
			for i in data[j]:
				if i == 'requirement' and req_num < len(data[j][i]) + 1:
					for k in range(req_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							requirement = Requirement()
							requirement.requirement = data[j][i][str(k)]
							process.requirements.append(requirement)
							req_num += 1
							break
						else:
							req_num += 1
							break
				if i == 'potential_failure_mode' and mod_num < len(data[j][i]) + 1:
					for k in range(mod_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_mode = FailureMode()
							failure_mode.failure_mode_name = data[j][i][str(k)]
							requirement.failure_modes.append(failure_mode)
							mod_num += 1
							break
						else:
							mod_num += 1
							break
				if i == 'potential_failure_effects' and effect_num < len(data[j][i]) + 1:
					for k in range(effect_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_effects = FailEffects()
							failure_effects.effects_content = data[j][i][str(k)]
							failure_mode.failure_effects.append(failure_effects)
							effect_num += 1
							break
						else:
							effect_num += 1
							break
				if i == 'severity' and sev_num < len(data[j][i]) + 1:
					for k in range(sev_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_effects.severity = data[j][i][str(k)]
							sev_num += 1
							break
						else:
							sev_num += 1
							break
				if i == 'classification' and cla_num < len(data[j][i]) + 1:
					for k in range(cla_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_mode.classification = data[j][i][str(k)]
							cla_num += 1
							break
						else:
							cla_num += 1
							break
				if i == 'potential_failure_causes' and cause_num < len(data[j][i]) + 1:
					for k in range(cause_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes = FailureCauses()
							failure_causes.causes_content = data[j][i][str(k)]
							failure_mode.failure_causes.append(failure_causes)
							cause_num += 1
							break
						else:
							cause_num += 1
							break
				if i == 'controls_prevention' and con_num < len(data[j][i]) + 1:
					for k in range(con_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.control_prevention = data[j][i][str(k)]
							con_num += 1
							break
						else:
							con_num += 1
							break
				if i == 'controls_detection' and con_det_num < len(data[j][i]) + 1:
					for k in range(con_det_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.control_detection = data[j][i][str(k)]
							con_det_num += 1
							break
						else:
							con_det_num += 1
							break
				if i == 'occurrence' and occ_num < len(data[j][i]) + 1:
					for k in range(occ_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.occurrence = data[j][i][str(k)]
							occ_num += 1
							break
						else:
							occ_num += 1
							break
				if i == 'detection' and det_num < len(data[j][i]) + 1:
					for k in range(det_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.detection = data[j][i][str(k)]
							det_num += 1
							break
						else:
							det_num += 1
							break
				if i == 'RPN' and rpn_num < len(data[j][i]) + 1:
					for k in range(rpn_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.RPN = data[j][i][str(k)]
							rpn_num += 1
							break
						else:
							rpn_num += 1
							break
				if i == 'recommended_action' and rec_num < len(data[j][i]) + 1:
					for k in range(rec_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.recommended_action = data[j][i][str(k)]
							rec_num += 1
							break
						else:
							rec_num += 1
							break
				if i == 'responsibility_completion_date' and res_num < len(data[j][i]) + 1:
					for k in range(res_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							failure_causes.responsibility_completion_date = data[j][i][str(k)]
							res_num += 1
							break
						else:
							res_num += 1
							break
			num -= 1


def insert_control(session, data):
	"""
	将控制计划数据导入到数据库
	:return:
	"""
	for j in data:
		process = session.query(Process).filter(Process.process_code == j).first()
		num = len(data[j]['methods']['evaluation_technique'])
		mach_num = pro_num = process_num = tol_num = eva_num = size_num = freq_num = con_num = rea_num = 1
		while num > 0:
			for i in data[j]:
				if i == 'machine' and mach_num < len(data[j][i]) + 1:
					for k in range(mach_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							machine = Machine()
							machine.machine_name = data[j][i][str(k)]
							process.machines.append(machine)
							mach_num += 1
							break
						else:
							mach_num += 1
							break
				if i == 'characteristics':
					for k in data[j][i]:
						if k == 'product' and pro_num < len(data[j][i][k]) + 1:
							for m in range(pro_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									product_features = ProductFeature()
									product_features.product_features = data[j][i][k][str(m)]
									product_features.excel_control = True
									process.product_features.append(product_features)
									pro_num += 1
									break
								else:
									pro_num += 1
									break
						if k == 'process' and process_num < len(data[j][i][k]) + 1:
							for m in range(process_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									process_features = ProcedureVariation()
									process_features.procedure_variation = data[j][i][k][str(m)]
									process_features.excel_control = True
									process.procedure_variations.append(process_features)
									process_num += 1
									break
								else:
									process_num += 1
									break
				if i == 'methods':
					for k in data[j][i]:
						if k == 'tolerance' and tol_num < len(data[j][i][k]) + 1:
							for m in range(tol_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									if data[j]['characteristics']['process'][str(pro_num - 1)]:
										process_features.tolerance = data[j][i][k][str(m)]
									else:
										product_features.tolerance = data[j][i][k][str(m)]
									tol_num += 1
									break
								else:
									tol_num += 1
									break
						if k == 'evaluation_technique' and eva_num < len(data[j][i][k]) + 1:
							for m in range(eva_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									control_plan = ControlPlan()
									control_plan.evaluation_technique = data[j][i][k][str(m)]
									if data[j]['characteristics']['process'][str(pro_num - 1)]:
										process_features.control_plans.append(control_plan)
									else:
										product_features.control_plans.append(control_plan)
									eva_num += 1
									break
								else:
									eva_num += 1
									break
						if k == 'size' and size_num < len(data[j][i][k]) + 1:
							for m in range(size_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									control_plan.size = data[j][i][k][str(m)]
									size_num += 1
									break
								else:
									size_num += 1
									break
						if k == 'freq' and freq_num < len(data[j][i][k]) + 1:
							for m in range(freq_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									control_plan.freq = data[j][i][k][str(m)]
									freq_num += 1
									break
								else:
									freq_num += 1
									break
						if k == 'control_methods' and con_num < len(data[j][i][k]) + 1:
							for m in range(con_num, len(data[j][i][k]) + 1):
								if data[j][i][k][str(m)]:
									control_plan.control_methods = data[j][i][k][str(m)]
									con_num += 1
									break
								else:
									con_num += 1
									break
				if i == 'reaction_plan' and rea_num < len(data[j][i]) + 1:
					for k in range(rea_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							control_plan.reaction_plan = data[j][i][str(k)]
							rea_num += 1
							break
						else:
							rea_num += 1
							break
			num -= 1


def insert_special(session, data):
	"""
	将特殊特性清单插入数据库
	:return:
	"""
	for j in data:
		process = session.query(Process).filter(Process.process_code == j).first()
		num = len(data[j]['process_special_characteristics'])
		pro_num = sym_num = reg_num = safety_num = func_num = fol_num = 1
		process_features = ProcedureVariation()
		while num > 0:
			for i in data[j]:
				if 'process_special_characteristics' == i and pro_num < len(data[j][i]) + 1:
					for k in range(pro_num, len(data[j][i]) + 1):
						process_features = ProcedureVariation()
						process_features.procedure_variation = data[j][i][str(k)]
						process.procedure_variations.append(process_features)
						pro_num += 1
						break

				if 'special_characteristics_symbol' == i and sym_num < len(data[j][i]) + 1:
					for k in range(sym_num, len(data[j][i]) + 1):
						process_features.special_symbol = data[j][i][str(k)]
						sym_num += 1
						break

				if 'regulatory_compliance' == i and reg_num < len(data[j][i]) + 1:
					for k in range(reg_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							process_features.regulatory_compliance = True
							reg_num += 1
							break
						else:
							reg_num += 1
							break

				if 'safety' == i and safety_num < len(data[j][i]) + 1:
					for k in range(safety_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							process_features.safety = True
							safety_num += 1
							break
						else:
							safety_num += 1
							break

				if 'function' == i and func_num < len(data[j][i]) + 1:
					for k in range(func_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							process_features.func = True
							func_num += 1
							break
						else:
							func_num += 1
							break

				if 'follow_process' == i and fol_num < len(data[j][i]) + 1:
					for k in range(fol_num, len(data[j][i]) + 1):
						if data[j][i][str(k)]:
							process_features.follow_process = True
							fol_num += 1
							break
						else:
							fol_num += 1
							break
			num -= 1


def insert_newfmea(data):
	"""
	插入新建的数据库
	"""
	with operation_database.session_scope() as session:
		for node in data:
			print(node)
			pro_flow = ProcessFlow()
			process = Process()
			if node['tags'][1] == '搬运':
				pro_flow.move = 'move'
			elif node['tags'][1] == '检验':
				pro_flow.inspect = 'inspect'
			elif node['tags'][1] == '储存':
				pro_flow.storage = 'storage'
			elif node['tags'][1] == '加工':
				pro_flow.procezo = 'procezo'
			process.process_name = node['tags'][0]
			process.process_code = node['text']
			for pro_feature in node['nodes'][0]['nodes']:
				product_feature = ProductFeature()
				product_feature.product_features = pro_feature['text']
				for variation in pro_feature['nodes'][0]['nodes']:
					pro_variation = ProcedureVariation()
					pro_variation.procedure_variation = variation['text']
					product_feature.procedure_variations.append(pro_variation)
				process.product_features.append(product_feature)
			for req in node['nodes'][1]['nodes']:
				requirement = Requirement()
				requirement.requirement = req['text']
				for mode in req['nodes'][0]['nodes']:
					failure_mode = FailureMode()
					failure_mode.failure_mode_name = mode['text']
					for cause in mode['nodes'][0]['nodes']:
						failure_cause = FailureCauses()
						failure_cause.causes_content = cause['text']
						failure_mode.failure_causes.append(failure_cause)
					for effect in mode['nodes'][1]['nodes']:
						failure_effect = FailEffects()
						failure_effect.effects_content = effect['text']
						failure_mode.failure_effects.append(failure_effect)
					requirement.failure_modes.append(failure_mode)
				process.requirements.append(requirement)
			pro_flow.processes.append(process)
			session.add(pro_flow)


if __name__ == '__main__':
	# engine = create_engine(Conf().msqconf_a(), echo=True)
	# create_tables(engine)
	insert_special()
