# coding: utf-8

import json

from nameko.rpc import rpc

from .db_relation import *
from .mysql_con import OperateDatabase

operation_db = OperateDatabase()


class DataOut(object):
	# 导出全部的数据
	name = "WholeJSON"

	@rpc
	def process(self):
		with operation_db.session_scope as session:
			processes = session.query(Process).all()
			process_list = []
			for process in processes:
				a = {"text": str(process.process_code + process.process_name), "nodes": []}
				a["nodes"].append({"text": "过程流程", "nodes": [{"text": process.process_flow}]})
				a["nodes"].append({"text": "输入变差", "nodes": [{"text": process.input_variations}]})
			# TODO 继续完善过程流程

	@rpc
	def pfmea(self):
		with operation_db.session_scope() as session:
			processes = session.query(Process).all()
			pfmea_list = []
			for process in processes:
				pfmea_json = json.loads(process.pfmea)
				pfl = {'text': str(process.process_code), "nodes": [
					{'test': '要求', "tags": [len(pfmea_json), process.process_name],
					 "nodes": [{
						 "text": "失效模式",
						 "nodes": [{
							 "text": pfmea_json['requirements'],
							 "nodes": [{
								 "text": pfmea_json['requirements']['nodes']['failure_mode']['text'],
								 "nodes": [{
									 "text": "失效影响",
									 "nodes": [{
										 "text": pfmea_json['requirements']['nodes']['failure_mode'][
											 'node']['causes_content']['text']
									 }]
								 }]
							 }]
						 }]
					 }]
					 }]
				       }
				pfmea_list.append(pfl)


class DataUpdate(object):
	# 检测传入的数据和数据库的数据并合并
	name = "JSONUpdate"

	# TODO 传入数据检测不同

	@rpc
	def pfmea(self):
		pass


class DataDelete(object):
	# 删除相关的数据
	name = "JSONDelete"

	# TODO 传入数据不同并删除
	@rpc
	def pfmea(self):
		pass
