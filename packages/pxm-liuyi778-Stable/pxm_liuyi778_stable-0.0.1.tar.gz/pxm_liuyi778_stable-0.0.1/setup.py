# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="pxm_liuyi778_Stable",
	version="1.0.4",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="这是一个Python编写的表格读写常用操作功能基础模块，使用了三种引擎进行封装,屏蔽各种引擎实现方式,统一方法",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/pxm",
	packages=["pxm_liuyi778_Stable"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.6',
	# 依赖
	install_requires=[
        "ColorInfo>=2.2.0",
        "openpyxl~=3.1.2"]
)
