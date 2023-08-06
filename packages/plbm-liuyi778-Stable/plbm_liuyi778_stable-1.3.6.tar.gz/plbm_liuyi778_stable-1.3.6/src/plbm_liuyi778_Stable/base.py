def ListRemoveNone(ls: list):
	"""
	移除列表中的空元素
	:param ls: 需要移除的列表
	:return: list
	"""
	tmp = []
	for i in ls:
		if str(i) != "" or str(i) != " " or i is not None:
			tmp.append(tmp)
	return tmp


def ListGetLen(ls: list, n: int):
	"""
	获取指定长度范围的元素列表
	:param n: 指定长度(移除小于该长度的元素)
	:param ls: 需要处理的列表
	:return: list
	"""
	tmp = []
	for i in ls:
		if len(i) > n:
			tmp.append(i)
	return tmp
