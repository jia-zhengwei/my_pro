# coding: utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.dispatch import receiver
from django_mysql import models as mod_json
from django.db import models
from django.db.models.signals import post_save


class Menu(models.Model):
    """菜单"""
    menu_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.menu_name



class Company(models.Model):
    """公司信息"""

    company_name = models.CharField(max_length=50, unique=True, blank=True)
    company_address = models.CharField(max_length=200, blank=True)
    company_email = models.EmailField(max_length=200, unique=True)
    company_phone = models.CharField(max_length=20, blank=True)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """扩展user用户"""

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    company_id = models.ForeignKey(Company, related_name='users', blank=True, null=True, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.email


class Project(models.Model):
    """项目"""

    project_name = models.CharField(max_length=100)
    company_id = models.ForeignKey(Company, related_name='projects', blank=True, null=True, on_delete=models.CASCADE)


class Fmea(models.Model):
    """fmea"""

    project_id = models.ForeignKey(Project, related_name='fmeas', blank=True, null=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyUser, related_name='fmeas', blank=True, null=True, on_delete=models.CASCADE)
    is_verify = models.BooleanField(default=False)
    is_pass = models.BooleanField(default=False)
    is_refuse = models.BooleanField(default=False)
    pfmea = mod_json.JSONField()

    class Meta:
        permissions = (
            ('verify_fmea', u'具有审核fmea权限'),
            ('create_fmea', u'具有开发fmea权限'),
            ('manage_fmea', u'具有管理fmea权限'),
        )



