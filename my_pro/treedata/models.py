from django.db import models
from django_mysql.models import JSONField


# class Group(models.Model):
#     """用户分组"""
#     group_name = models.CharField(max_length=50)
#     descripe = models.CharField(max_length=255)
#     company = models.ForeignKey("Company")


# class User(models.Model):
#     """用户信息"""
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     is_admin = models.BooleanField()
#     is_super = models.BooleanField()
#     log_time = models.TimeField(auto_now_add=True)


# class Company(models.Model):
#     """公司信息"""
#     company_name = models.CharField(max_length=255)
#     company_email = models.CharField(max_length=255)
#     company_address = models.CharField(max_length=255)
#     telephone = models.CharField(max_length=11)


class Project(models.Model):
    """项目信息"""
    pro_name = models.CharField(max_length=255)
    descripe = models.CharField(max_length=500)
    create_time = models.TimeField()
    documents = JSONField()


class Process(models.Model):
    """过程编号"""
    process_name = models.CharField(max_length=100, null=False)
    process_code = models.CharField(max_length=50)
    process_flow = JSONField()


# class Record(models.Model):
#     """用户操作记录"""
#     descripe = JSONField()
#     user = models.ForeignKey("User")
#     project = models.ForeignKey("Document")


class Document(models.Model):
    """项目文件"""
    descripe = JSONField()
    project = models.ForeignKey("Project")

