#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   iptables.py
@Time    :   2022-08-11 11:55
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   防火墙管理
"""

from subprocess import getstatusoutput
from sys import exit

from src.plbm_liuyi778_Stable.Jurisdiction import Jurisdiction
from src.plbm_liuyi778_Stable.Service import ServiceManagement
from src.plbm_liuyi778_Stable.Cmd import ComMand
from .logger import ColorLogger


class IpTables:
	def __init__(self, password=None, logs=False, log_file=None, port=80, source=None, zone=None, direction="INPUT"):
		"""
		Iptables防火墙软件配置
		:param password: 主机密码(root用户不需要)
		:param logs: 是否显示详细信息
		"""
		self.log_file = log_file
		self.logs = logs
		self.logger = ColorLogger(file=log_file, txt=logs)
		self.cmd = ComMand(password=password, logs=logs)
		ju = Jurisdiction(passwd=password, logs=logs)
		if not ju.verification(name='IpTables'):
			self.logger.error("sudo权限验证失败,请检查密码是否正确或者账号是否有权限")
			exit(1)

		self.agreement = 'TCP'
		self.port = int(port)
		if source is None:
			source = "0.0.0.0/0"
		self.source = source
		if zone is None:
			zone = 'public'
		self.zone = zone
		self.ok = False
		# 设置方向，默认： 进口
		if direction != "INPUT":
			direction = ""
		self.direction = direction
		# 记录已配置的端口列表
		self.port_list = []
		# 记录端口详细情况
		self.port_dic = {}
		# 查看已配置且接受的端口列表
		self.port_accept_list = []
		# 记录ID和端口的关系
		self.port_id_port = {}
		self.service_name = 'ipsec'
		self.service = ServiceManagement(service=self.service_name, password=password, log=logs)
	
	def open_port_appoint_ip(self):
		"""
		开放特定端口给特定主机
		:return:
		"""
		pass
	
	def save(self):
		"""
		保存更改
		"""
		self.cmd.sudo(cmd='iptables-save', name='保存更改')
		if int(self.cmd.code) == 0:
			self.logger.info("保存成功")
		else:
			self.logger.warning("保存失败")

	def set_port_appoint_source(self, agreement=None, port=None, source=None, mode="ACCEPT"):
		"""
		设置特定IP接受或拒绝访问特定端口
		:param agreement: 协议(tcp/udp/icmp)
		:param port: 端口号
		:param source: 设置源地址
		:param mode: 设置策略模式，拒绝(REJECT)或者接受(ACCEPT)
		:return: 配置结果(bool)
		"""
		if agreement is None:
			agreement = self.agreement
		if port is None:
			port = self.port
		if source is None:
			source = self.source
		cmd = "iptables -A INPUT -p {0} -s {1} --dport {2} -j {3}".format(agreement, source, port, mode)
		name = "开放端口: %s" % port
		if str(mode).lower() == 'REJECT'.lower():
			name = "关闭端口: %s" % port
		self.cmd.sudo(cmd=cmd, name=name)
		if int(self.cmd.code) != 0:
			if self.logs:
				mess = str(name) + "失败"
				self.logger.error(mess)
	
	def open_port_all_ip(self, agreement=None, port=None):
		"""
		开放端口给所有IP
		:param agreement: 协议(tcp/udp),默认：TCP
		:param port: 端口号,默认: 80
		:return: 配置结果
		"""
		if agreement is None:
			agreement = self.agreement
		if port is None:
			port = self.port
		cmd = "iptables -A INPUT -p {0} --dport {1} -j ACCEPT ".format(agreement, port)
		print(cmd)
		c = getstatusoutput(cmd)
		if c[0] == 0:
			print("开放成功: ", port)
			self.save()
			return True
		else:
			print("开放失败: ", port)
		return False
	
	def delete_port(self, port):
		"""_summary_
		通过端口删除策略
		Args:
			port (int): 需要删除的端口
		"""
		self.get()
		del_id_list = []
		for id_ in self.port_id_port:
			port_ = self.port_id_port[id_]
			if int(port_) == int(port):
				del_id_list.append(id_)
		if del_id_list:
			self.delete_port_to_id(r_id=del_id_list, auto=True)
	
	def delete_port_to_id(self, r_id=None, auto=False):
		"""
		通过ID删除策略
		:param auto: 是否使用自动模式
		:param r_id: 需要删除的端口id列表
		:return:
		"""
		if r_id is None:
			r_id = []
		if not auto:
			print("使用对答模式")
			print(getstatusoutput("iptables -L -n --line-numbe")[1])
			id_ = input("请输入需要删除的策略ID值(整数),每个ID之间使用空格间隔\n")
			r_id = str(id_).split(' ')
		del_sum = 0
		for id_del in r_id:
			self.logger.debug("\n删除源id: %s" % id_del)
			if int(del_sum) != 0:
				print("由于条目发生变化, 源规则ID [ {0} ] 减去 [ {1} ]".format(id_del, del_sum))
			id_del = int(id_del) - int(del_sum)
			# info = "iptables -L -n --line-number | grep ^{0}".format(id_del)
			cmd = "iptables -D INPUT {0}".format(id_del)
			if self.cmd.sudo(cmd=cmd, terminal=False):
				self.logger.info('删除成功: %s' % id_del)
			else:
				self.logger.error("删除失败: %s" % id_del)
			del_sum += 1
	
	def get(self):
		"""
		获取已经开放的端口
		:return:
		"""
		cmd = "iptables -L -n --line-number | grep -v ^Chain | grep -v ^num | sed 's/\t/_/g'"
		g = getstatusoutput(cmd)
		if g[0] == 0:
			# print("执行查询成功")
			port_str_list = str(g[1]).split('\n')
			for port_str in port_str_list:
				port_str_list = str(port_str).replace(' ', '_').split('_')
				result = []
				if len(port_str_list) >= 2:
					for i in port_str_list:
						if str(i) != '':
							result.append(i)
					port_ = str(result[7]).split(':')[1]
					# 记录ID与端口的dic
					self.port_id_port[result[0]] = port_
					if port_ not in self.port_list:
						self.port_dic[port_] = result
						self.port_list.append(port_)
						if result[1] == 'ACCEPT':
							self.port_accept_list.append(port_)
		else:
			print("执行查询失败")
	
	def start(self):
		"""
		启动服务
		:return:
		"""
		return self.service.restart()
	
	def status(self):
		"""
		获取当前状态
		:return:
		"""
		res = self.service.status()
		return res
	
	def clean_all(self):
		"""
		删除所有规则
		:return:
		"""
		sum_ = 0
		for cmd in ["iptables -X", "iptables -F", "iptables -Z"]:
			if self.cmd.sudo(cmd=cmd, terminal=False):
				sum_ += 1
		if int(sum_) == 3:
			self.logger.info("清除成功")
		else:
			self.logger.error("清除失败")


if __name__ == "__main__":
	up = IpTables()
	up.status()
