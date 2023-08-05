#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/28 17:30
# @Author  : xgy
# @Site    : 
# @File    : pdfcheck_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
from csp.command.cli import csptools
# from csp.thirdparty import PdfCheck


# 一级命令 CSPtools pdfcheck
@csptools.group("pdfcheck")
def pdfcheck():
    """
    pdf文件缺陷检测命令

    \b
    csp pdfcheck 'commands' -h 获取子命令使用帮助
    """

## pdf 缺陷检测
@pdfcheck.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--in_file", help="待检测pdf文件", required=True)
def check(version, port, c_name, r, in_file):
    """
    检测命令

    \b
    使用示例：csp pdfcheck check -i 'pdf文件路径'
    """
    from csp.thirdparty import PdfCheck
    pdf_check = PdfCheck(version=version, port=port, c_name=c_name, reload=r)
    result = pdf_check.check(in_file)
    print(result)


if __name__ == '__main__':
    print("start")
