# -*- encoding: utf-8 -*-
"""
@File    :   FileManagement.py
@Time    :   2022/04/13 20:16:27
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   文件管理
"""
from os import path, makedirs
from shutil import rmtree, copy2, move
from subprocess import getstatusoutput
from .logger import ColorLogger


class FileManagement:
	def __init__(self, target=None, log=True, log_file=None, txt_log=False):
		"""
		文件管理模块
		:param target: 管理目标
		:param log: 是否开启日志
		:param log_file: 日志文件
		:param txt_log: 是否开启文件日志
		"""
		self.log = log
		self.md5 = ''
		self.target = target
		self.logger = ColorLogger(file=log_file, txt=txt_log)

	def rmdir(self, target=None, ignore_errors=True):
		"""
		删除文件夹
		:param target: 需要删除的路径
		:param ignore_errors: 是否忽略错误
		:return: bool(当不存在或者删除程序则返回True，否则返回False)
		"""
		if target is None:
			target = self.target
		if path.isdir(target):
			try:
				rmtree(path=target, ignore_errors=ignore_errors)
				return True
			except Exception as e:
				self.logger.error(str(e))
				return False
		return True

	def move(self, src, dst, cover=False):
		"""
		移动文件
		:return:
		"""
		if path.exists(src):
			if cover:
				self.rmdir(target=dst)
			try:
				move(src=str(src), dst=str(dst))
				return True
			except Exception as e:
				self.logger.error(str(e))
				return False

	def copyfile(self, src, dst, cover=False):
		"""
		复制文件
		:param src: 源文件/文件夹路径
		:param dst: 目标文件路径或者文件夹路径
		:param cover: 当目标存在是否覆盖(建议关闭)
		:return:
		"""
		ok = False
		if path.exists(src):
			if cover and path.exists(dst):
				self.move(src=dst, dst=str('%s_move' % dst))
			try:
				copy2(src=str(src), dst=str(dst))
				ok = True
			except Exception as e:
				self.logger.error(str(e))
			if ok:
				self.rmdir(target=str('%s_move' % dst))
		return ok

	def mkdir_p(self, target=None, mode=644):
		"""
		创建递归文件夹
		:param mode: 权限模式
		:param target: 需要创建的路径,默认使用实例化对象
		:return:
		"""
		if target is None:
			target = self.target
		try:
			makedirs(name=target, mode=mode, exist_ok=True)
			return True
		except Exception as e:
			self.logger.error(str(e))
			return False

	def get_md5(self, filename=None):
		"""
		获取文件MD5值
		:param filename: 需要获取MD5的文件路径
		:return: 获取结果(bool),具体值请通过 self.md5 获取
		"""
		get = False
		if filename is None and self.target:
			filename = self.target
		if path.isfile(filename):
			c = "md5sum %s | awk '{print $1}'" % filename
			res = getstatusoutput(c)
			if res[0] == 0:
				self.md5 = res[1]
				get = True
		else:
			self.logger.warning('文件不存在: %s' % filename)
		return get


if __name__ == "__main__":
	fm = FileManagement(target='/etc/hosts')
	fm.get_md5()
	fm.mkdir_p(target='/home/liumou', mode=666)
	fm.rmdir(target='/home/liumou')
