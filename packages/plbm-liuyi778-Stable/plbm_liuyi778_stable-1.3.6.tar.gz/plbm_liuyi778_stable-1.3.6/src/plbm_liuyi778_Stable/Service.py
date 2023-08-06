#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Service.py
@Time    :   2022-10-23 23:00
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from . import Jurisdiction, Command
from .logger import ColorLogger
from .OsInfo import OsInfo
from os import path


class ServiceManagement:
	def __init__(self, service, password, log=True):
		"""
		服务管理
		:param service: 服务名称
		:param password: 密码
		:param log: 是否开启文本日志
		"""
		self.log = log
		self.password = password
		self.service = service
		file = path.join(OsInfo().home_dir, 'ServiceManagement.log')
		self.logger = ColorLogger(file=file, txt=log, class_name=self.__class__.__name__)
		self.ju = Jurisdiction(passwd=password, logs=log)
		self.cmd = Command(password=password, logs=log)

	def _sudo(self):
		"""
		检查是否已有sudo权限
		:return:
		"""
		if self.ju.verification(name='ServiceManagement'):
			return True
		return False

	def start(self, service=None, name=None):
		"""
		启动服务
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		if service is None:
			service = self.service
		if name is None:
			name = service
		c = str("systemctl start {}".format(service))
		return self.cmd.sudo(cmd=c, name="Start %s" % name)

	def disable(self, service=None, name=None):
		"""
		关闭开机自启
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		if service is None:
			service = self.service
		if name is None:
			name = service
		c = str("systemctl disable {}".format(service))
		return self.cmd.sudo(cmd=c, name="Start %s" % name)

	def enable(self, service=None, name=None):
		"""
		设置开机自启
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		if service is None:
			service = self.service
		if name is None:
			name = service
		c = str("systemctl enable {}".format(service))
		return self.cmd.sudo(cmd=c, name="Start %s" % name)

	def stop(self, service=None, name=None):
		"""
		停止服务
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		if service is None:
			service = self.service
		if name is None:
			name = service
		c = str("systemctl stop {}".format(service))
		res = self.cmd.sudo(cmd=c, name="Stop %s" % name)
		if self.log:
			if res:
				self.logger.info("停止成功: %s" % name)
			else:
				self.logger.error("停止失败: %s" % name)
		return res

	def status(self, service=None, name=None):
		"""
		停止服务
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 是否运行中(bool)
		"""
		if service is None:
			service = self.service
		if name is None:
			name = str(service)
		c = str("systemctl -all | grep %s | awk '{print $4}'" % service)
		res = self.cmd.getout_sudo(cmd=c, name=name, mess_failed="已停止", mess_ok="运行中")
		if self.cmd.code == 0:
			if str(res) == str('running'):
				return True
		return False

	def restart(self, service=None, name=None, reload=False):
		"""
		重启服务
		:param reload: 是否重载服务配置
		:param name: 服务名称(中文)
		:param service: 服务名称
		:return: 启动结果(bool)
		"""
		if service is None:
			service = self.service
		if name is None:
			name = service
		if reload:
			c = str("systemctl daemon-reload")
			self.cmd.sudo(cmd=c, name='重载服务配置')
		c = str("systemctl restart {}".format(service))
		res = self.cmd.sudo(cmd=c, name="Restart %s" % name)
		if self.log:
			if res:
				self.logger.info("重启成功: %s" % name)
			else:
				self.logger.error("重启失败: %s" % name)
		return res

	def existence(self, service=None, name=None):
		"""
		判断服务是否存在
		:param name: 服务名称(中文)
		:param service: 服务名称,后面必须带service，例如：docker.service
		:return:是否存在(bool)
		"""
		if service is None:
			service = self.service
		c = "systemctl -all | grep %s | awk '{print $1}'" % service
		res = self.cmd.getout_sudo(cmd=c, name=name)
		ok = False
		if self.cmd.code == 0:
			if str(res) == str(service):
				ok = True
		if self.log:
			if ok:
				self.logger.info("服务存在: %s" % name)
			else:
				self.logger.warning("服务不存在: %s" % name)
		return ok
