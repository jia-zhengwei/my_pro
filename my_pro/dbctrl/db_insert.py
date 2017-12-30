# coding: utf-8

from database_relation import *
from mysql_con import OperateDatabase
from nameko.rpc import rpc

operatedb = OperateDatabase()


class InsertDB(object):
	# 插入数据库
	name = "insert_db"

	@rpc
	def process(data):
		"""
		:param data: 过程流程
		:return: None
		"""
		pass

	@rpc
	def insert_pfmea(session, data):
		"""
		:param data: PFMEA
		:return: None
		"""
		for i in data:
			num = len(data[i]['potential_failure_causes'])


