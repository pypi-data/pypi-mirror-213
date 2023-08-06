# -*- encoding: utf-8 -*-
"""
@File    :   NetStatus.py
@Time    :   2022/04/13 11:19:25
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   网络管理
"""
import socket
from os import path, getcwd
from sys import platform

from . import FileManagement, Command, get
from .logger import ColorLogger


class NetworkCardInfo:
	def __init__(self, eth=None, debug=False):
		"""
		获取本地网卡信息
		:param eth: 设置网卡名,当不设置的时候则自动检测
		"""
		# Dns地址列表
		self.dns = None
		self.debug = debug
		self.eth = eth
		self.os = platform.lower()
		self.linux = False
		if self.os.lower() == 'linux'.lower():
			self.linux = True
		# 设置网关地址
		self.gw = None
		# 设置IP地址
		self.ip = None
		# 设置子网信息
		self.sub = None
		# 设置mac地址
		self.mac = None
		# 设置子网掩码
		self.mask = 24
		# 设置连接名称
		self.connect = None
		# 连接速率
		self.rate = None
		self.cmd = Command(password="pd")
		self.logger = ColorLogger()

	def show(self):
		"""
		显示网卡信息
		:return:
		"""
		self.logger.info("Eth_self.eth :", self.eth)
		self.logger.info("Gateway_self.gw : ", self.gw)
		self.logger.info("IP_self.ip: ", self.ip)
		self.logger.info("Subnet Mask_self.mask : ", self.mask)
		self.logger.info("Dns List_self.dns: ", str(self.dns))
		self.logger.info("Mac _self.mac : ", self.mac)
		self.logger.info("Connect Rate_self.rate: ", self.rate)
		self.logger.info("Connect Name_self.connect: ", self.connect)

	def get_dev_list(self):
		"""
		获取网卡列表并检测网卡信息
		:return:
		"""
		c = "nmcli device  | awk '{print $1}'"
		g = self.cmd.getout(cmd=c).split("\n")
		if self.eth is not None:
			if str(self.eth) in g:
				self.logger.info("The set device name is in the existing list")
				return True
			else:
				self.logger.warning("Device not found: ", self.eth)
				self.logger.debug("Automatic detection will be used")
		self.getip_request()
		return False

	def get_all(self):
		"""
		获取所有网卡信息
		:return: 获取结果(bool)
		"""
		existence = self.get_dev_list()
		if self.linux:
			if not existence:
				# 使用自动检测网卡信息
				self.logger.debug("Use automatic network card detection")
				try:
					# 如果设置的网卡不存在，则使用自动的方式检测网卡信息
					dev_ = str("""ip r | grep default | grep %s | awk '{print $5}'""" % self.sub)
					# 获取网卡名称
					self.eth = self.cmd.getout(cmd=dev_)
				except Exception as e:
					print(e)
					return False
			else:
				# 检测指定网卡信息
				self.logger.debug("Detect the specified network card information")
				if not self.getip_dev():
					self.logger.error("Query failed")
					return False
		else:
			self.logger.error("当前设备不是Linux")
			return False
		# 获取连接参数
		connect_arg_ = "nmcli device show  %s | grep IP4" % self.eth
		connect_arg = self.cmd.getout(connect_arg_).split("\n")
		# 子网掩码
		self.mask = int(str(connect_arg[0]).split("/")[1])
		# 网关查询命令
		self.gw = connect_arg[1]
		# 设备信息
		search_ = """nmcli device show  %s | grep GENERAL | awk '{print $2}'""" % self.eth
		search_info = self.cmd.getout(cmd=search_).split("\n")
		# Mac地址
		self.mac = search_info[2]
		# 连接速率
		self.rate = search_info[4]
		# 连接名称
		self.connect = search_info[5]
		# Dns列表
		d_ = """nmcli device show  %s | grep IP4 | grep DNS | awk '{print $2}'""" % self.eth
		self.dns = str(self.cmd.shell(cmd=d_)).split('\n')
		self.show()

	def getip_dev(self):
		"""
		使用指定设备的方式获取IP
		:return:
		"""
		c = "nmcli device show  %s | grep IP4 | sed -n 1p | awk '{print $2}'" % self.eth
		info = self.cmd.getout(c)
		# info 会得到这样的数据: 10.16.17.103/24
		if self.cmd.code == 0:
			self.logger.debug("query was successful")
			ni = str(info).split("/")
			self.ip = ni[0]
			self.mask = ni[1]
			return True
		else:
			self.logger.error("Query failed. Please check the connection status of the network card")
		return False

	def getip_request(self):
		"""
		使用网络请求的方式获取IP
		:return:
		"""
		try:
			csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			csock.connect(('119.29.29.29', 53))
			(addr, port) = csock.getsockname()
			csock.close()
			self.ip = addr
			tu = str(self.ip).split('.')
			self.sub = str("%s.%s.%s." % (tu[0], tu[1], tu[2]))
			return True
		except Exception as e:
			self.logger.error(str(e))
			return False


class NetStatus:
	def __init__(self, ip=None, port=80, log_file=None, txt_log=False):
		"""
		网络工具，用于判断网络是否正常
		:param ip: 需要判断的IP
		:param port:  需要判断的端口. Defaults to None.
		:param log_file: 日志文件
		:param txt_log: 是否开启文本日志
		"""
		self.ip = ip
		self.port = port
		self.status = False
		#
		self.headers = {}
		self.headers = get.headers
		self.cmd = Command(password='Gxxc@123')
		self.fm = FileManagement()
		self.logger = ColorLogger(file=log_file, txt=txt_log)

	def ping_status(self, server=None):
		"""
		使用ping检测网络连接
		:param server: 设置服务器地址. Defaults to self.ip.
		:return:
		"""
		self.status = False
		if server is None:
			server = self.ip
		self.logger.info('正在检测： %s' % server)
		cmd = 'ping %s -c 5' % server
		if platform.lower() == 'win32':
			cmd = 'ping %s ' % server
		if self.cmd.shell(cmd=cmd):
			self.logger.info("Ping 连接成功: %s" % server)
			self.status = True
		else:
			self.logger.error("Ping 连接失败: %s" % server)
		return self.status

	def downfile(self, url, filename=None, cover=False, md5=None):
		"""
		下载文件
		:param url: 下载链接
		:param filename: 保存文件名,默认当前目录下以URL最后一组作为文件名保存
		:param cover: 是否覆盖已有文件. Defaults to False.
		:param md5: 检查下载文件MD5值
		:return: 下载结果(bool)
		"""
		if filename is None:
			filename = str(url).split("/")[-1]
			filename = path.join(getcwd(), filename)
		filename = path.abspath(filename)
		if path.exists(filename):
			if not cover:
				self.logger.info("检测到已存在路径: %s" % filename)
				self.logger.info("放弃下载： %s" % url)
				return True
			self.logger.debug("检测到已存在路径,正在删除...")
			c = 'rm -rf ' + filename
			if self.cmd.shell(cmd=c):
				self.logger.info("删除成功: %s" % filename)
			else:
				self.logger.warning("删除失败,跳过下载")
				return False
		c = str("wget -c -O %s %s" % (filename, url))
		self.cmd.shell(cmd=c, terminal=False)
		if int(self.cmd.code) == 0:
			self.logger.info("下载成功: %s" % filename)
			if md5:
				get_ = self.fm.get_md5(filename=filename)
				if get_:
					if str(md5).lower() == str(self.fm.md5).lower():
						return True
				else:
					return False
			return True
		self.logger.error("下载失败: %s" % filename)
		self.logger.error("下载链接: ", url)
		self.logger.error("保存路径: ", filename)
		return False


if __name__ == "__main__":
	up = NetStatus()
	up.ping_status(server='baidu.com')
