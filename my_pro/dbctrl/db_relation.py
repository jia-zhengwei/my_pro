# coding: utf-8

# from datetime import datetime
import datetime

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Table, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

user_group = Table('tbl_user_group', Base.metadata,
                   Column('user_id', Integer, ForeignKey('User.id'), nullable=False, primary_key=True),
                   Column('group_id', Integer, ForeignKey('Group.id'), nullable=False, primary_key=True),
                   Column('role_id', Integer, ForeignKey('Role.id'), nullable=False, primary_key=True)
                   )

group_project = Table('tbl_group_project', Base.metadata,
                      Column('group_id', Integer, ForeignKey('Group.id'), nullable=False, primary_key=True),
                      Column('project_id', Integer, ForeignKey('Project.id'), nullable=False, primary_key=True)
                      )

role_file = Table('tbl_role_file', Base.metadata,
                  Column('role_id', Integer, ForeignKey('Role.id'), nullable=False, primary_key=True),
                  Column('file_id', Integer, ForeignKey('Document.id'), nullable=False, primary_key=True)
                  )

group_menu = Table('tbl_group_menu', Base.metadata,
                   Column('group_id', Integer, ForeignKey('Group.id'), nullable=False, primary_key=True),
                   Column('menu_id', Integer, ForeignKey('Menu.id'), nullable=False, primary_key=True)
                   )


class Data(Base):
	"""添加的伪数据"""

	__tablename__ = 'Data'

	id = Column(Integer, primary_key=True, autoincrement=True)
	fake_data = Column(String(50))
	feature = Column(Boolean, default=False)
	requirement = Column(Boolean, default=False)
	variation = Column(Boolean, default=False)
	process_id = Column(Integer, ForeignKey('Process.id'))
	user_id = Column(Integer, ForeignKey('User.id'))


class Menu(Base):
	"""系统菜单"""
	__tablename__ = 'Menu'

	id = Column(Integer, primary_key=True, autoincrement=True)
	icon = Column(String(50))
	menu_name = Column(String(50))
	groups = relationship('Group', secondary=group_menu, backref='menus', cascade='all')


class Company(Base):
	"""公司信息"""
	__tablename__ = 'Company'

	id = Column(Integer, primary_key=True, autoincrement=True)
	company_name = Column(String(255))
	company_email = Column(String(255))
	company_address = Column(String(255))
	telephone = Column(String(50))
	groups = relationship('Group', backref='Company', cascade='all')
	projects = relationship('Project', backref='Company', cascade='all')


class Project(Base):
	"""项目"""
	__tablename__ = 'Project'

	id = Column(Integer, primary_key=True, autoincrement=True)
	pro_name = Column(String(255))
	descripe = Column(String(500))
	create_time = Column(DateTime, default=datetime.datetime.now())
	company_id = Column(Integer, ForeignKey('Company.id'))
	groups = relationship('Group', secondary=group_project, backref='projects', cascade='all')
	documents = relationship('Document', backref='Project', cascade='all')


class Document(Base):
	"""项目文件 管理文件"""
	__tablename__ = 'Document'

	id = Column(Integer, primary_key=True, autoincrement=True)
	description = Column(JSON)
	project_id = Column(Integer, ForeignKey('Project.id'))
	processes = relationship('Process', backref='Document', cascade='all')
	roles = relationship('Role', secondary=role_file, backref='files', cascade='all')
	records = relationship('Record', backref='Document', cascade='all')


class User(Base):
	"""用户信息"""
	__tablename__ = 'User'

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String(50))
	password = Column(String(50))
	email = Column(String(100))
	is_admin = Column(Boolean, default=False)
	is_super = Column(Boolean, default=False)
	is_active = Column(Boolean, default=False)
	log_time = Column(DateTime, default=datetime.datetime.now())
	# log_out_time = Column(DateTime, default=datetime.datetime.now() + datetime.timedelta(minutes=1))
	company_id = Column(Integer, ForeignKey('Company.id'))
	group_id = Column(Integer, ForeignKey('Group.id'))
	records = relationship('Record', backref='User', cascade='all')
	groups = relationship('Group', secondary=user_group, backref='User', cascade='all')


class Group(Base):
	"""用户分组"""
	__tablename__ = 'Group'

	id = Column(Integer, primary_key=True, autoincrement=True)
	group_name = Column(String(50))
	descripe = Column(String(255))
	roles = relationship('Role', secondary=user_group, backref='groups', cascade='all')
	company_id = Column(Integer, ForeignKey('Company.id'))


class Role(Base):
	"""组的权限设定"""
	__tablename__ = 'Role'

	id = Column(Integer, primary_key=True, autoincrement=True)
	role = Column(String(255))
	is_del = Column(Boolean, default=False)
	is_edit = Column(Boolean, default=False)
	is_add = Column(Boolean, default=False)
	descripe = Column(String(255))


class Record(Base):
	"""
	用户操作记录
	"""

	__tablename__ = 'Record'

	id = Column(Integer, primary_key=True, autoincrement=True)
	descripe = Column(String(255))
	sub_time = Column(DateTime, default=datetime.datetime.now())
	user_id = Column(Integer, ForeignKey('User.id'))
	document_id = Column(Integer, ForeignKey('Document.id'))


class Process(Base):
	"""
	过程编号
	过程名称
	"""

	__tablename__ = "Process"

	id = Column(Integer, primary_key=True, autoincrement=True)
	process_name = Column(String(100), nullable=False)
	process_code = Column(String(50))
	process_flow = Column(JSON, nullable=False)
	file_id = Column(Integer, ForeignKey('Document.id'))
	product_features = relationship('ProductFeature', backref='Process', cascade='all')
	input_variations = Column(JSON, nullable=False)
	procedure_variations = relationship('ProcedureVariation', backref='Process')
	pfmea = relationship("PFMEA", backref="Process", cascade="all")
	machines = relationship('Machine', backref='Process', cascade='all')
	parent_id = Column(Integer, ForeignKey('Process.id'))
	children = relationship("Process", lazy="joined", join_depth=2)


class ProductFeature(Base):
	"""
	产品特性
	"""

	__tablename__ = "ProductFeature"

	id = Column(Integer, primary_key=True, autoincrement=True)
	product_features = Column(String(500), nullable=False)
	tolerance = Column(String(100))
	excel_control = Column(Boolean, default=False)
	process_id = Column(Integer, ForeignKey("Process.id"))
	control_plans = relationship('ControlPlan', backref='ProductFeature', cascade='all')
	procedure_variations = relationship('ProcedureVariation', backref='ProductFeature', cascade='all')


class ProcedureVariation(Base):
	"""
	过程变差/过程特性(工艺特性)
	"""

	__tablename__ = "ProcedureVariation"

	id = Column(Integer, primary_key=True, autoincrement=True)
	procedure_variation = Column(JSON, default={
		"tolerance": None,
		"procedure_variation": None,
		"special_symbol": None,
		"regulatory_compliance": False,
		"safety": None,
		"func": None,
		"follow_process": False,
		"excel_control": False
	})
	process_id = Column(Integer, ForeignKey("Process.id"))
	control_plans = relationship('ControlPlan', backref='ProcedureVariation', cascade='all')
	product_feature_id = Column(Integer, ForeignKey('ProductFeature.id'))


class Machine(Base):
	"""
	设备工装
	"""

	__tablename__ = "Machine"

	id = Column(Integer, primary_key=True, autoincrement=True)
	machine_name = Column(String(500))
	process_id = Column(Integer, ForeignKey("Process.id"))


class ControlPlan(Base):
	"""
	控制计划
	"""

	__tablename__ = "ControlPlan"

	id = Column(Integer, primary_key=True, autoincrement=True)
	evaluation_technique = Column(String(100))
	size = Column(String(100))
	freq = Column(String(100))
	control_methods = Column(String(100))
	reaction_plan = Column(String(100))
	product_feature_id = Column(Integer, ForeignKey('ProductFeature.id'))
	procedure_feature_id = Column(Integer, ForeignKey('ProcedureVariation.id'))


class PFMEA(Base):
	"""PFMEA
	这里的pfmea json字段仅为当前的
	"""
	__tablename__ = "PFMEA"

	id = Column(Integer, primary_key=True, autoincrement=True)
	process_id = Column(Integer, ForeignKey("Process.id"))
	pfmea = Column(JSON, default={
		"requirements": {
			"failure_mode": {
				"causes_content": {
					"action_taken_result": {
						"severity": None,
						"occurrence": None,
						"detection": None,
						"RPN": None,
						"responsibility": None,
						"completion_date": None,
					},
					"occurrence": None,
					"detection": None,
					"control_prevention": None,
					"control_detection": None,
					"RPN": None,
					"recommended_action": None,
				},

				"effects_content": None,
				"severity": None,
				"classification": None,
			}
		}
	})


if __name__ == '__main__':
	db_str = "mysql://root:jzw@127.0.0.1:3306/fmea?charset=utf8mb4"
	engine = create_engine(db_str, echo=True)
	Base.metadata.create_all(engine)
	# Base.metadata.drop_all(engine)
