# -*- encoding: utf-8 -*-
from pathlib import Path
from ColorInfo import ColorLogger


def _exists(file, flist=None):
	"""
	判断文件是否存在及文件格式是否符合要求
	:param file: 文件名称
	:param flist: 文件格式列表定义
	:return:
	"""
	if flist is None:
		flist = ["xls", "xlsx", "et"]
	logger = ColorLogger()
	path = Path(file)
	if not path.exists():
		logger.error("文件不存在: ", file)
		return False
	if not path.is_file():
		logger.error("该对象不是文件")
		return False
	file_format = str(file).split('.')[-1]
	if str(file_format) in flist:
		return True
	logger.error("不支持的文件格式: ", file_format)
	return False

