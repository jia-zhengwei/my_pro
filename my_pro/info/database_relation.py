# coding: utf-8

# from datetime import datetime
import datetime

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, ForeignKey, Table, JSON, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()



user_group = Table('tbl_user_group', Base.metadata,
                   Column('user_id', Integer, ForeignKey('User.id'), nullable=False, primary_key=True),
                   Column('group_id', Integer, ForeignKey('Group.id'), nullable=False, primary_key=True),
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
    process_id = Column(Integer, ForeignKey('Process.id', ondelete=True))
    user_id = Column(Integer, ForeignKey('User.id', ondelete=True))


class Menu(Base):
    """系统菜单"""
    __tablename__ = 'Menu'

    id = Column(Integer, primary_key = True, autoincrement = True)
    icon = Column(String(50))
    menu_name = Column(String(50))
    parent_id = Column(Integer, ForeignKey('Menu.id'))
    children = relationship("Menu", lazy="joined", join_depth=2)
    groups = relationship('Group', secondary = group_menu, backref = 'menus', cascade='all')


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
    processes = relationship('Process', backref='Project', cascade='all')


class Document(Base):
    """项目文件"""
    __tablename__ = 'Document'

    id = Column(Integer, primary_key = True, autoincrement = True)
    filename = Column(String(255))
    descripe = Column(String(500))
    project_id = Column(Integer, ForeignKey('Project.id'))
    roles = relationship('Role', secondary = role_file, backref = 'files', cascade='all')
    records = relationship('Record', backref='Document', cascade='all')


class User(Base):
    """用户信息"""
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(50))
    email = Column(String(100))
    is_active = Column(Boolean, default = False)
    is_super = Column(Boolean, default=False)
    log_time = Column(DateTime, default=datetime.datetime.now())
    company_id = Column(Integer, ForeignKey('Company.id'))
    records = relationship('Record', backref='User', cascade='all')
    groups = relationship('Group', secondary=user_group, backref='User', cascade='all')

class Group(Base):
    """用户分组"""
    __tablename__ = 'Group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50))
    descripe = Column(String(255))
    company_id = Column(Integer, ForeignKey('Company.id'))
    users = relationship('User', secondary=user_group, backref='Group', cascade='all')


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


class ProcessFlow(Base):
    """
    过程流程
    加工、搬运、存储、检验
    """

    __tablename__ = "ProcessFlow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # todo 修改成JSON字段形式
    flow = Column(String(50))
    procezo = Column(String(50))
    move = Column(String(50))
    storage = Column(String(50))
    inspect = Column(String(50))
    processes = relationship('Process', backref='ProcessFlow', cascade='all', passive_deletes=True)


class Process(Base):
    """
    过程编号
    过程名称
    """

    __tablename__ = "Process"

    id = Column(Integer, primary_key=True, autoincrement=True)
    process_name = Column(String(100), nullable=False)
    process_code = Column(String(50))
    process_flow_id = Column(Integer, ForeignKey('ProcessFlow.id'))
    project_id = Column(Integer, ForeignKey('Project.id'))
    product_features = relationship('ProductFeature', backref='Process', cascade='all',
                                    passive_deletes=True)
    input_variations = relationship('InputVariation', backref='Process', cascade='all',
                                    passive_deletes=True)
    procedure_variations = relationship('ProcedureVariation', backref='Process', cascade='all',
                                        passive_deletes=True)
    requirements = relationship('Requirement', backref='Process', cascade='all', passive_deletes=True)
    machines = relationship('Machine', backref='Process', cascade='all', passive_deletes=True)
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
    process_id = Column(Integer, ForeignKey("Process.id", ondelete=True))
    control_plans = relationship('ControlPlan', backref='ProductFeature', cascade='all',
                                 passive_deletes=True)
    procedure_variations = relationship('ProcedureVariation', backref='ProductFeature', cascade='all',
                                        passive_deletes=True)
    faliure_modes = relationship('FailureMode', backref='ProductFeatures', cascade='all',
                                 passive_deletes=True)


class InputVariation(Base):
    """
    输入变差
    """

    __tablename__ = "InputVariation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_variation = Column(String(500), nullable=False)
    process_id = Column(Integer, ForeignKey("Process.id", ondelete=True))


class ProcedureVariation(Base):
    """
    过程变差/过程特性(工艺特性)
    """

    __tablename__ = "ProcedureVariation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tolerance = Column(String(100))
    procedure_variation = Column(String(500), nullable=False)
    special_symbol = Column(String(100))
    regulatory_compliance = Column(Boolean, default=False)
    safety = Column(Boolean, default=False)
    func = Column(Boolean, default=False)
    follow_process = Column(Boolean, default=False)
    excel_control = Column(Boolean, default=False)
    process_id = Column(Integer, ForeignKey("Process.id", ondelete=True))
    control_plans = relationship('ControlPlan', backref='ProcedureVariation', cascade='all',
                                 passive_deletes=True)
    product_feature_id = Column(Integer, ForeignKey('ProductFeature.id', ondelete=True, onupdate=True))
    faliure_modes = relationship('FailureMode', backref='ProcedureVariation', cascade='all',
                                 passive_deletes=True)


class Machine(Base):
    """
    设备工装
    """

    __tablename__ = "Machine"

    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_name = Column(String(500))
    process_id = Column(Integer, ForeignKey("Process.id", ondelete=True))


class Requirement(Base):
    """
    过程需求/要求
    """

    __tablename__ = "Requirement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    requirement = Column(String(500), nullable=False)
    process_id = Column(Integer, ForeignKey("Process.id", ondelete=True))
    failure_modes = relationship('FailureMode', backref='Requirement', cascade='all',
                                 passive_deletes=True)


class FailureMode(Base):
    """
    失效模式
    失效模式的名称
    """

    __tablename__ = "FailureMode"

    id = Column(Integer, primary_key=True, autoincrement=True)
    failure_mode_name = Column(String(500), nullable=False)
    classification = Column(String(10))
    rpn = Column(Integer)
    requirement_id = Column(Integer, ForeignKey('Requirement.id', ondelete=True, onupdate=True))
    feature_id = Column(Integer, ForeignKey('ProductFeature.id', ondelete=True, onupdate=True))
    variation_id = Column(Integer, ForeignKey('ProcedureVariation.id', ondelete=True, onupdate=True))
    failure_causes = relationship('FailureCauses', backref='FailureMode', cascade='all',
                                  passive_deletes=True)
    failure_effects = relationship('FailEffects', backref='FailureMode', cascade='all',
                                   passive_deletes=True)


class FailureCauses(Base):
    """
    潜在失效原因
    """

    __tablename__ = "FailureCauses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    causes_content = Column(String(500), nullable=False)
    occurrence = Column(Integer)
    detection = Column(Integer)
    control_prevention = Column(String(500))
    control_detection = Column(String(500))
    RPN = Column(Integer)
    recommended_action = Column(String(500))
    responsibility_completion_date = Column(DateTime)
    failure_mode = Column(Integer, ForeignKey('FailureMode.id', onupdate=True, ondelete=True))
    action_taken_results = relationship('ActionTakenResult', backref='FailureCauses', cascade='all',
                                        passive_deletes=True)


class FailEffects(Base):
    """
    潜在失效影响
    """

    __tablename__ = "FailEffects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    effects_content = Column(String(500))
    severity = Column(Integer)
    failure_mode_id = Column(Integer, ForeignKey('FailureMode.id', ondelete=True, onupdate=True))


class ActionTakenResult(Base):
    """
    实施结果
    """

    __tablename__ = "ActionTaken"

    id = Column(Integer, primary_key=True, autoincrement=True)
    severity = Column(Integer)
    occurrence = Column(Integer)
    detection = Column(Integer)
    RPN = Column(Integer)
    responsibility = Column(String(500))
    completion_date = Column(DateTime, default=None)
    failure_causes_id = Column(Integer, ForeignKey('FailureCauses.id', onupdate=True, ondelete=True))


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
    product_feature_id = Column(Integer, ForeignKey('ProductFeature.id', ondelete=True, onupdate=True))
    procedure_feature_id = Column(Integer, ForeignKey('ProcedureVariation.id', ondelete=True, onupdate=True))


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    db_str = 'mysql://root:Callkin@123456@192.168.1.10:3306/fmea?charset=utf8mb4'
    engine = create_engine(db_str, echo=True)
    create_tables(engine)
    # drop_tables(engine)
