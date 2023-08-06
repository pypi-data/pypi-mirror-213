# -*- encoding: utf-8 -*-
import string


def GetDic():
	"""
	获取数字和字母的对应关系,例如: 0:A, 1:B
	:return:
	"""
	zm = string.ascii_uppercase
	cellDic = {}
	s = 0
	for i in zm:
		cellDic[s] = str(i).upper()
	for i in zm:
		for m in zm:
			k = str(i) + str(m)
			cellDic[s] = k.upper()
			s += 1
	return cellDic
