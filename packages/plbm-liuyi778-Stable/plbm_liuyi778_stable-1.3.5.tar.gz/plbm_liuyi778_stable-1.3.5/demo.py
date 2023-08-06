# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2022-10-24 22:45
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from src.plbm_liuyi778_Stable import ServiceManagement
from ColorInfo import ColorLogger


class ServiceManager:
	def __init__(self, services, password):
		self.services = services
		self.manager = ServiceManagement(service=services, password=password)
		self.logger = ColorLogger(class_name=self.__class__.__name__)

	def restart(self):
		if self.manager.restart(reload=True):
			self.logger.info("服务重启成功")
		else:
			self.logger.warning("服务重启失败")


if __name__ == "__main__":
	demo = ServiceManager(services="vsftpd", password="demo")
	demo.restart()
