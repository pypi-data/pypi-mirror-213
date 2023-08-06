# -*- encoding: utf-8 -*-
"""
@File    :   DPKG.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from .Cmd import Command
from .logger import ColorLogger
from os import path


class DpkgManagement:
	def __init__(self, password, log=False, terminal=False):
		"""
		Apt 管理
		:param password: 主机密码
		:param log: 是否启用日志
		:param terminal: 是否使用终端执行命令(针对个别Linux发行部才起作用)
		"""
		# 当前查询版本
		self.local_package_version = ''
		# 当前包名称
		self.local_package_name = ''
		# 当前获取状态
		self.get_status = False
		self.log = log
		self.terminal = terminal
		self.password = password
		self.cmd = Command(password=self.password, cmd='which apt', terminal=self.terminal, logs=self.log)
		self.logger = ColorLogger()
		# 需要安装的安装包文件信息
		self.file_install = ''
		# 可安装的文件列表
		self.install_list = []
		# 格式错误的文件列表
		self.format_err = []
		# 不存在的文件列表
		self.not_err = []

	def _show(self):
		"""
		显示信息
		:return:
		"""
		if self.install_list:
			self.logger.info('可安装的文件列表如下')
			for i in self.install_list:
				print(i)
		if self.format_err:
			self.logger.warning('格式错误的文件列表如下')
			for i in self.format_err:
				print(i)
		if self.not_err:
			self.logger.error('不存在的文件列表如下')
			for i in self.not_err:
				print(i)

	def _add_file(self, file):
		"""
		检测并添加文件
		:param file:
		:return: 安装信息(str)
		"""
		f_name = str(file).split('.')[-1]
		if str(f_name).lower() == 'deb':
			if path.isfile(file):
				self.file_install = str(self.file_install) + " " + str(file)
				self.install_list.append(file)
			else:
				self.logger.error('列表中检测到不存在的安装包: %s' % str(file))
				self.not_err.append(file)
		else:
			self.logger.warning('列表中检测到格式不正确的文件: %s' % str(file))
			self.format_err.append(file)

	def install(self, deb_file=None, name=None):
		"""
		安装本地安装包文件
		:param name: 任务名称
		:param deb_file:传入需要安装的deb文件路径(建议绝对路径),多个文件请使用列表传入
		:return: 安装结果(bool)
		"""
		self.install_list = []
		if type(deb_file) == list:
			for i in deb_file:
				self.logger.debug("Check :", str(i))
				self._add_file(file=i)
		else:
			if type(deb_file) == str:
				self._add_file(file=deb_file)
		if self.install_list:
			self.logger.info("Installing %s ..." % self.file_install)
			cmd = str("dpkg -i %s" % self.file_install)
			if name is None:
				name = 'Install %s Packages' % len(self.install_list)
			return self.cmd.sudo(cmd=cmd, name=name)
		else:
			self.logger.error('没有找到可安装的文件信息')
			self._show()
		return False

	def configure(self):
		"""
		:return: 配置结果(bool)
		"""
		return self.cmd.sudo(cmd="dpkg --configure -a", name='Continue configuring all Packages')

	def uninstall(self, pac, name=None):
		"""

		:param name: 任务名称
		:param pac:需要卸载的包，例如：docker.io
		:return: 卸载结果(bool)
		"""
		cmd = str("dpkg -P %s" % pac)
		if name is None:
			name = 'UnInstall %s' % pac
		self.logger.info("UnInstalling %s ..." % name)
		return self.cmd.sudo(cmd=cmd, name=name)

	def check_local_pac_version(self, pac=None, pac2=None, pac_v=None):
		"""
		检查已安装软件版本是否正确(local_package_name 记录当前包名称/local_package_version 记录当前版本)
		:param pac2: 软件包关键词2(如果传入该值则使用两个关键词进行匹配)
		:param pac: 包名(不支持仅传入关键词)
		:param pac_v: 标准版本
		:return: 是否一致(Bool)
		"""
		self.get_status = False
		cmd = """dpkg -l | grep %s | awk '{print $1,$2,$3}'""" % pac
		if pac2 is not None:
			cmd = """dpkg -l | grep %s | grep %s | awk '{print $1,$2,$3}'""" % (pac, pac2)
		info = self.cmd.getout(cmd=cmd).split(' ')
		if self.cmd.code == 0:
			self.local_package_name = info[1]
			self.local_package_version = info[2]
			self.logger.debug('already installed: ', pac)
			if str(info[0]) == 'ii':
				self.get_status = True
				self.logger.debug("Normal status")
				if str(info[1]).lower() == str(pac).lower():
					self.logger.debug("Matching succeeded")
					if str(info[2]) == str(pac_v):
						return True
					else:
						self.logger.warning("Version mismatch")
				else:
					self.logger.warning("Software matching failed")
			else:
				self.logger.warning("Damaged")
		return False

	def get_local_pac_version(self, pac, pac2=None):
		"""
		获取本地包版本,通过(local_package_version)获取值
		:param pac2: 软件包关键词2(如果传入该值则使用两个关键词进行匹配)
		:param pac: 包名称
		:return: 获取结果(bool)
		"""
		self.check_local_pac_version(pac=pac, pac_v='get_local_pac_version', pac2=pac2)
		return self.get_status
