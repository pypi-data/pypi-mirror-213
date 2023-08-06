#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Jurisdiction.py
@Time    :   2022/04/25 16:54:45
@Author  :   村长
@Version :   1.0
@Contact :   liumou.site@qq.com
@Desc    :   权限验证模块
"""

from os import system
from subprocess import getoutput

from .logger import ColorLogger
from src.plbm_liuyi778_Stable.OsInfo import OsInfo


class Jurisdiction:
	def __init__(self, passwd, logs=False, log_file=None):
		"""
		权限验证
		:param passwd: 设置主机密码
		:param logs: 是否启用文本日志
		:param log_file: 日志文件
		"""
		self.log_file = log_file
		self.logs = logs

		self.loggers = ColorLogger(class_name=self.__class__.__name__)
		if self.logs:
			self.loggers = ColorLogger(class_name=self.__class__.__name__,
			                           txt=self.logs, file=self.log_file)
		self.passwd = passwd
		self.super_permissions = False
		self.os_type = OsInfo().os_type

	def reset_pd(self):
		"""
		重置密码
		:return:
		"""
		username = getoutput('echo $USER')
		for i in range(2):
			status = self._check()
			if status:
				return True
			else:
				self.passwd = input("请输入用户[ %s ]登录密码:\n" % username)
		self.loggers.error("重试次数超过程序设置值")
		return False

	def _check(self):
		"""
		检查密码是否正确
		:return:
		"""
		c = "echo %s | sudo -S touch /d" % self.passwd
		d = "echo %s | sudo -S rm -f /d" % self.passwd
		res = system(c)
		if str(res) == '0':
			system(d)
			self.loggers.info("密码正确")
			return True
		self.loggers.error('密码错误或者当前用户无sudo权限')
		return False

	def verification(self, name, reset=False):
		"""
		检测sudo权限是否能够获取并设置正确的密码, 最终密码可以通过实例变量获取(self.passwd)
		:param name: 调用的任务名称
		:param reset: 是否使用对话模式设置正确密码(默认False)
		:return: 是否取得sudo权限(True取得/False未取得)
		"""
		username = getoutput('echo $USER')
		uid = getoutput("echo $UID")
		if str(username).lower() == 'root' or str(uid) == '0':
			if self.logs:
				self.loggers.info('已处于root权限')
			return True
		if self.os_type.lower() == 'uos'.lower():
			self.developer()
		else:
			self.super_permissions = True
		if self.super_permissions:
			if reset:
				return self.reset_pd()
			else:
				return self._check()
		return False

	def developer(self):
		"""_summary_
		检查是否开启开发者模式
		Returns:
			bool: 是否开启开发者
		"""
		dev_file = "/var/lib/deepin/developer-install_modes/enabled"
		dev1 = str(getoutput(cmd="cat %s") % dev_file).replace(" ", '').replace('\n', '')

		dev_file2 = "/var/lib/deepin/developer-install_mode/enabled"
		dev2 = str(getoutput(cmd="cat %s") % dev_file2).replace(" ", '').replace('\n', '')

		dev_file3 = "cat /var/lib/deepin/developer-mode/enabled"
		dev3 = str(getoutput(cmd=dev_file3)).replace(" ", '').replace('\n', '')

		terminal_mode = False
		if dev1 == "1" or dev2 == "1" or dev3 == "1":
			terminal_mode = True
		elif str(getoutput('echo $UID')) != '0' and str(getoutput('echo $USER')) == "root" or str(
				getoutput('echo $UID')) == '0':
			terminal_mode = True
		self.super_permissions = terminal_mode
		if self.super_permissions:
			self.loggers.info('已开启开发者')
			return True
		else:
			self.loggers.warning('开发者未开启')
		return False


if __name__ == "__main__":
	ju = Jurisdiction(passwd='1')
	if ju.verification(name='Demo'):
		print('密码验证正确')
	else:
		print('密码验证失败')
