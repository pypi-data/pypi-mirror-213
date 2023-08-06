import unittest
from plbm.NetManagement import NetManagement
from unittest.mock import MagicMock


class TestCon(unittest.TestCase):
	def test_GetConInfo(self):
		n = NetManagement()
		IpMock = MagicMock(return_value="10.1.1.18")
		info = n.GetConIp
		info = IpMock
		ip = IpMock("wifi")
		self.assertEqual(ip, "10.1.1.18")
		IpMock.assert_called_with("wifi")


if __name__ == '__main__':
	unittest.main()
