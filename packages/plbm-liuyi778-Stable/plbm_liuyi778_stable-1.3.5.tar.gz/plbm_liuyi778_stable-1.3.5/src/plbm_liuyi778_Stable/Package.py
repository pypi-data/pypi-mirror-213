#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   Package.py
@Time    :   2022-10-23 01:40
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   Linux包管理工具
"""
from os import path, system

from .logger import ColorLogger
from .Cmd import ComMand
from .Yum import YumManager
from .Dpkg import DpkgManagement
from .AptManage import AptManagement
from .Jurisdiction import Jurisdiction


class PackageManagement:
	def __init__(self, password, logs=True, file=None, package=None):
		"""
		Linux包管理模块
		:param password: 主机密码
		:param logs: 是否开启日志
		:param file: 需要安装的文件
		:param package: 需要安装的包
		"""
		self.package = package
		self.file = file
		self.logs = logs
		self.password = password
		self.cmd = ComMand(password=password, logs=logs)
		self.ju = Jurisdiction(passwd=password, logs=logs)
		self.install_tools = 'apt'
		self.manger = AptManagement(password=password, log=logs)
		self.local = DpkgManagement(password=password, log=logs)
		if int(system('which yum')) == 0:
			self.install_tools = 'yum'
		self.logger = ColorLogger(file=file, txt=logs, class_name=self.__class__.__name__)
		self.init()
	
	def init(self):
		"""
		初始化
		:return:
		"""
		if self.install_tools.lower() == 'yum':
			self.manger = YumManager(password=self.password, log_file=self.file, log=self.logs)
	
	def check_sudo(self):
		"""
		检测是否已有sudo权限
		:return:
		"""
		return self.ju.verification(name='PackageManger - check_sudo')
	
	def install(self, package, update=False):
		"""
		在线安装服务
		:param update: 是否更新索引再安装
		:param package: 需要安装的包
		:return: 安装结果(bool)
		"""
		return self.manger.install(pac=package, update=update)
	
	def _format_check(self):
		"""
		检查文件格式
		:return:
		"""
		format_ = str(self.file).split('.')[-1]
		if str(format_).lower() == 'deb' or str(format_).lower() == 'rpm':
			return True
		if self.logs:
			self.logger.error("文件格式不正确: {0}".format(self.file))
		return False
	
	def install_local_file_single(self, file=None):
		"""
		安装单个本地安装包文件
		:param file: 需要安装的文件,只能传入一个安装包文件
		:return: 安装结果(bool)
		"""
		if file:
			self.file = file
		if self._format_check():
			if path.isfile(file):
				return self.manger.local_install_f(file=file)
			else:
				if self.logs:
					self.logger.error("文件不存在: {0}".format(file))
		return False
	
	def install_local_matching(self, file=None):
		"""
		安装多个本地安装包文件(不检查是否存在文件)
		:param file: 需要安装的文件,可以使用通配符(后缀必须使用文件格式),例如： /root/*.deb
		:return: 安装结果(bool)
		"""
		if file:
			self.file = file
		if self._format_check():
			return self.manger.local_install_f(file=file)
		return False
	
	def uninstall(self, package=None):
		"""
		使用(apt purge/yum remove)移除软件包
		:param package: 需要移除的软件名称
		:return:
		"""
		if package:
			self.package = package
		return self.local.uninstall(pac=self.package)
	
	def uninstall_local(self, package=None, name=None):
		"""
		使用(dpkg -P /rpm -e)移除软件包
		:param package: 需要移除的包
		:param name: 名称
		:return: 卸载结果(bool)
		"""
		if package:
			self.package = package
		if name is None:
			name = self.package
		return self.local.uninstall(pac=package, name=name)
	
	def installed(self, pac=None):
		"""
		查询服务是否安装
		:return:
		"""
		if pac is None:
			pac = self.package
		ok = self.manger.installed(pac=pac)
		if ok:
			self.logger.info('已安装: %s' % pac)
		else:
			self.logger.warning('未安装: %s' % pac)
		return ok
	
	def upgrade(self, update_index=True, dist=True):
		"""
		升级系统
		:param update_index: 是否更新索引
		:param dist: 温柔的更新(针对apt)
		:return:
		"""
		if self.install_tools.lower() == 'apt':
			self.manger = AptManagement(password=self.password, log=self.logs)
			if dist:
				return self.manger.upgrade_dist(update=update_index)
			else:
				return self.manger.upgrade(update=update_index)
		else:
			self.manger = YumManager(password=self.password, log=self.logs)
			return self.manger.update(update=update_index)
