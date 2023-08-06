#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py
@Time    :   2023-02-17 23:36
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
from ColorInfo import ColorLogger

from src.pxm_liuyi778_Stable import Read


class DemoRead:
	def __init__(self, filename="xls/demo.xlsx"):
		"""

		:param filename:
		"""
		self.filename = filename
		self.logger = ColorLogger(class_name=self.__class__.__name__)
		self.r = Read(filename=self.filename)  # 读取文件
		self.r.Set(sheet_index=1)  # 设置Sheet索引值1（也就是第二个Sheet)
		self.r.GetAll()  # 获取所有数据
	
	def all(self):
		if self.r.Err:
			self.logger.error("读取失败: ", r.Err)
		else:
			self.logger.info("数据读取成功")
			print(self.r.DataR)
	
	def line(self):
		data = self.r.CutLine(0)  # 截取第一行并获取最终结果
		print("第一行的数据: ", data.DataR)
	
	def lineRange(self):
		self.r.GetLineRange(start=1, end=4)
		print("获取lineRange数据: ", self.r.Data)
	
	def start(self):
		self.all()
		self.line()
		self.info()
		self.lineRange()
	
	def info(self):
		print(f"当前工作簿数据总列数: {self.r.InfoCols}")
		print(f"当前工作簿数据总行数: {self.r.InfoRows}")
		print(f"当前工作簿索引值: {self.r.InfoSheet}")
		print(f"当前工作簿名称: {self.r.InfoSheetName}")


if __name__ == "__main__":
	d = DemoRead()
	d.start()
