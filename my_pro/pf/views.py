# coding: utf-8
import json
import os

from django.core.files import File
from django.http import (FileResponse, HttpResponse, JsonResponse)
from django.shortcuts import render
from pyexcel_xlsx import get_data

from info.data import DataOperation
from info.database_relation import *
from info.insert_database import (insert_process, insert_newfmea, insert_pfmea, insert_control, insert_special)
from info.insert_excel import (output_process, output_pfmea)
from info.mysql_con import OperateDatabase

operation_database = OperateDatabase()


def fs_data_import(request):
	"""
	进入提交数据的页面
	"""
	return render(request, 'data.html')


def fs_data_update(request):
	"""
	 进入编辑数据页面
	"""
	json_data = jsonData()

	return render(request, 'treeview.html', {'json_data': json.dumps(json_data)})


def newData(request):
	"""
	跳转到编辑数据的页面
	:param request:
	:return:
	"""
	if request.method == 'GET':

		return render(request, 'newData.html')
	else:
		return render(request, 'login01.html')


def addForm(request):
	"""
	跳转到添加修改数据的页面
	:param request:
	:return:
	"""
	if request.method == 'GET':
		process_id = request.GET.get('id')
		Node = request.GET['Node']
		return render(request, 'addForm.html', {'process_id': process_id, 'node': Node})
	else:
		return render(request, 'login01.html')


def data_list(request):
	"""
	编辑数据时，选择框改变，输出相应的数据到二级选择框里
	:param request:
	:return:
	"""
	if request.method == 'GET':
		data_type = request.GET['type']
		pro_id = request.GET['pro_id']
		with operation_database.session_scope() as session:
			if data_type == 'mode':
				mode_list = []
				req = []
				requires = session.query(Requirement).filter(Requirement.process_id == pro_id).all()
				for require in requires:
					req.append(dict(req=require.requirement, id=require.id))
				for require in requires:
					modes = session.query(FailureMode).filter(FailureMode.requirement_id == require.id).all()
					for mode in modes:
						mode_list.append(mode.failure_mode_name)
				data = {'req': req, 'modes': mode_list}
				return JsonResponse(data)
			elif data_type == 'variation':
				variations = session.query(ProcedureVariation).filter(ProcedureVariation.process_id == pro_id).all()
				mode_list = []
				for variation in variations:
					mode_list.append(variation.procedure_variation)
				data = {'modes': mode_list}
				return JsonResponse(data)
			elif data_type == 'product':
				products = session.query(ProductFeature).filter(ProductFeature.process_id == pro_id).all()
				mode_list = []
				for product in products:
					mode_list.append(product.product_features)
				data = {'modes': mode_list}
				return JsonResponse(data)
			elif data_type == 'require':
				requirements = session.query(Requirement).filter(Requirement.process_id == pro_id).all()
				mode_list = []
				for requirement in requirements:
					mode_list.append(requirement.requirement)
				data = {'modes': mode_list}
				return JsonResponse(data)
			elif data_type == 'cause':
				req = []
				mode_list = []
				requirements = session.query(Requirement).filter(Requirement.process_id == pro_id).all()
				for require in requirements:
					failure_modes = session.query(FailureMode).filter(FailureMode.requirement_id == require.id).all()
					for failure_mode in failure_modes:
						req.append(dict(req=failure_mode.failure_mode_name, id=failure_mode.id))
						failure_causes = session.query(FailureCauses) \
							.filter(FailureCauses.failure_mode == failure_mode.id).all()
						for failure_cause in failure_causes:
							mode_list.append(failure_cause.causes_content)
				data = {'req': req, 'modes': mode_list}
				return JsonResponse(data)
			elif data_type == 'effect':
				req = []
				mode_list = []
				requirements = session.query(Requirement).filter(Requirement.process_id == pro_id).all()
				for require in requirements:
					failure_modes = session.query(FailureMode).filter(FailureMode.requirement_id == require.id).all()
					for failure_mode in failure_modes:
						req.append(dict(req=failure_mode.failure_mode_name, id=failure_mode.id))
						failure_effects = session.query(FailEffects) \
							.filter(FailEffects.failure_mode_id == failure_mode.id).all()
						for failure_effect in failure_effects:
							mode_list.append(failure_effect.effects_content)
				data = {'req': req, 'modes': mode_list}
				print(data)
				return JsonResponse(data)

	else:
		msg = '请求失败'
		return HttpResponse(msg)


def treeData_create(request):
	"""
	传递nodes数据，写入数据库
	"""
	msg = '创建成功'
	if request.method == 'POST':
		data = json.loads(request.body)
		insert_newfmea(data['node'])
		return HttpResponse(msg)
	else:
		return False


def treeData_add(request):
	"""
	treevie添加支点,并且将添加的支点加入数据库
	:param request:
	:return:
	"""
	msg = ''
	if request.method == 'POST':
		data = json.loads(request.body)
		with operation_database.session_scope() as session:
			if data['type'] == 'mode':
				requirement = session.query(Requirement).filter(Requirement.id == int(data['req'])).first()
				mode = FailureMode()
				mode.failure_mode_name = data['text']
				requirement.failure_modes.append(mode)
				msg = '添加成功'
			elif data['type'] == 'variation':
				process = session.query(Process).filter(Process.id == int(data['pro_id'])).first()
				variation = ProcedureVariation()
				variation.procedure_variation = data['text']
				process.procedure_variations.append(variation)
				msg = '添加成功'
			elif data['type'] == 'product':
				process = session.query(Process).filter(Process.id == int(data['pro_id'])).first()
				product = ProductFeature()
				product.product_features = data['text']
				process.product_features.append(product)
				msg = '添加成功'
			elif data['type'] == 'require':
				process = session.query(Process).filter(Process.id == int(data['pro_id'])).first()
				require = Requirement()
				require.requirement = data['text']
				process.requirements.append(require)
				msg = '添加成功'
			elif data['type'] == 'cause':
				failure_mode = session.query(FailureMode).filter(FailureMode.id == int(data['req'])).first()
				failure_cause = FailureCauses()
				failure_cause.causes_content = data['text']
				failure_mode.failure_causes.append(failure_cause)
				msg = '添加成功'
			elif data['type'] == 'effect':
				failure_mode = session.query(FailureMode).filter(FailureMode.id == int(data['req'])).first()
				failure_effects = FailEffects()
				failure_effects.effects_content = data['text']
				failure_mode.failure_effects.append(failure_effects)
				msg = '添加成功'
			info = {'msg': msg, 'data': jsonData()}
			return JsonResponse(info)
	else:
		return render(request, 'index.html')


def import_record(request):
	"""
	查阅导入数据记录
	:param request:
	:return:
	"""
	if request.method == 'GET':
		with operation_database.session_scope() as session:
			records = session.query(Record).order_by(Record.sub_time.desc()).all()
			num = 0
			record_list = []
			for record in records:
				num += 1
				data = {}
				user = session.query(User).filter(User.id == record.user_id).first()
				data['num'] = num
				data['record'] = record
				data['user'] = user.username
				record_list.append(data)
			return render(request, 'record.html', {'record_list': record_list})
	else:
		return render(request, 'login01.html')


def treeData_update(request):
	"""
	修改treeeview支点，并且修改数据库
	:param request:
	:return:
	"""
	msg = ''
	if request.method == 'POST':
		text = request.POST.get('text')
		node = request.POST.get('Node')
		parentNode = request.POST.get('parentNode')
		with operation_database.session_scope() as session:
			if parentNode == "产品特性":
				product_feature = session.query(ProductFeature).filter(ProductFeature.id == node).first()
				product_feature.product_features = text
			elif parentNode == "工艺特性":
				procedure = session.query(ProcedureVariation).filter(ProcedureVariation.id == node).first()
				procedure.procedure_variation = text
			elif parentNode == '要求':
				requirement = session.query(Requirement).filter(Requirement.id == node).first()
				requirement.requirement = text
			elif parentNode == '失效模式':
				failure_mode = session.query(FailureMode).filter(FailureMode.id == node).first()
				failure_mode.failure_mode_name = text
			elif parentNode == '失效原因':
				failure_cause = session.query(FailureCauses).filter(FailureCauses.id == node).first()
				failure_cause.causes_content = text
			elif parentNode == '失效影响':
				failure_effect = session.query(FailEffects).filter(FailEffects.id == node).first()
				failure_effect.effects_content = text
	return HttpResponse(msg)


def treeData_del(request):
	"""
	删除支点并且删除数据库(process)
	:param request:
	:return:
	"""
	msg = ""
	if request.method == "POST":
		node = request.POST.get("Node")
		parentNode = request.POST.get("parentNode")
		with operation_database.session_scope() as session:
			if parentNode == "产品特性":
				product_feature = session.query(ProductFeature).filter(ProductFeature.id == node).first()
				session.delete(product_feature)
				msg = "删除成功"
			elif parentNode == "工艺特性":
				procedure_feature = session.query(ProcedureVariation).filter(ProcedureVariation.id == node).first()
				session.delete(procedure_feature)
				msg = "删除成功"
			elif parentNode == '要求':
				requirement = session.query(Requirement).filter(Requirement.id == node).first()
				session.delete(requirement)
				msg = "删除成功"
			elif parentNode == '失效模式':
				failure_mode = session.query(FailureMode).filter(FailureMode.id == node).first()
				session.delete(failure_mode)
				msg = "删除成功"
			elif parentNode == '失效影响':
				failure_effect = session.query(FailEffects).filter(FailEffects.id == node).first()
				session.delete(failure_effect)
				msg = "删除成功"
			elif parentNode == '失效原因':
				failure_cause = session.query(FailureCauses).filter(FailureCauses.id == node).first()
				session.delete(failure_cause)
				msg = "删除成功"
	return HttpResponse(msg)


def insert_database(request):
	"""
	插入数据到数据库
	:return:
	"""
	if request.method == 'POST':
		msg = '导入的数据文件有误，重新检查文件名'
		file_type = request.POST.get('type')
		obj = request.FILES.get('file')
		myfile = File(obj)
		filename = myfile.name
		data = get_data(obj)
		desperation = DataOperation(data)
		new_data = desperation.update_data()
		user_id = request.session['id']
		with operation_database.session_scope() as session:
			user = session.query(User).filter(User.id == user_id).first()
			record = Record()
			record.user_id = user.id
			if file_type == "control":
				if user.control_excel:
					msg = '该文件已经导入数据库，重复导入会导致数据重复'
				else:
					user.control_excel = True
					record.filename = filename
					data = desperation.data_control(new_data)
					insert_control(data)
					msg = '导入数据成功'
			elif file_type == "process":
				if user.process_excel:
					msg = '该文件已经导入数据库，重复导入会导致数据重复'
				else:
					user.process_excel = True
					record.filename = filename
					data = desperation.data_process(new_data)
					insert_process(data)
					msg = '导入数据成功'
			elif file_type == "pfmea":
				if user.failure_excel:
					msg = '该文件已经导入数据库，重复导入会导致数据重复'
				else:
					user.failure_excel = True
					record.filename = filename
					data = desperation.data_failure(new_data)
					insert_pfmea(data)
					msg = '导入数据成功'
			elif file_type == "special":
				if user.special_excel:
					msg = '该文件已经导入数据库，重复导入会导致数据重复'
				else:
					user.special_excel = True
					record.filename = filename
					data = desperation.data_special(new_data)
					insert_special(data)
					msg = '导入数据成功'
			session.add(record)
		return HttpResponse(msg)
	else:
		return render(request, 'login01.html')


def file_download_page(request):
	"""
	进入导出数据页面
	:param request:
	:return:
	"""
	return render(request, 'outdata.html')


def build_excel(request):
	"""
	导出数据到excel
	:param request:
	:return:
	"""

	def file_iterator(fn, chunk_size=512):
		with open(fn, 'rb') as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break

	excel_type = request.POST.get('excel_type')
	if excel_type == 'process':
		output_process()
		download_path = '过程流程.xlsx'
	elif excel_type == 'pfmea':
		output_pfmea()
		download_path = 'pfmea.xlsx'
	else:
		download_path = ''
	response = FileResponse(file_iterator(download_path))
	response['Content-Length'] = os.path.getsize(download_path)
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(download_path)
	return response
