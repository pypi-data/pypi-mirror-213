#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/8 09:21
# @Author  : liny
# @Site    :
# @File    : ocr_cli.py
# @Software: IDEA
# @python version: 3.7.4
"""

import click
from csp.command.cli import csptools
# from csp.thirdparty import Ocr


# 一级命令 CSP ocr
@csptools.group("ocr")
def ocr():
    """
    OCR命令，包括文本识别、表格识别、证照识别等子命令

    \b
    csp ocr 'commands' -h 获取子命令使用帮助
    """


## 纯文本抽取
@ocr.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--file", help="图片路径", required=True)
def ocr_text(version, port, c_name, r, file):
    """
    纯文本识别命令

    \b
    使用示例：csp ocr ocr-text -i '图片路径'
    """
    from csp.thirdparty import Ocr
    ocrclient = Ocr(version, port, c_name, reload=r)
    result = ocrclient.ocr_text(file)
    print(result)

## OCR表格识别
@ocr.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--file", help="图片路径", required=True)
def ocr_table(version, port, c_name, r, file):
    """
    表格识别命令

    \b
    使用示例：csp ocr ocr-table -i '图片路径'
    """
    from csp.thirdparty import Ocr
    ocrclient = Ocr(version=version, port=port, c_name=c_name, reload=r)
    result = ocrclient.ocr_table(file)
    print(result)

## OCR固定格式的电子证照识别
@ocr.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-o", "--code", help="证照类型，idcard/train_ticket/audit/safety_production_license其一", required=True)
@click.option("-i", "--file", help="图片路径", required=True)
def ocr_fixed_file(version, port, c_name, r, code, file):
    """
    证照识别命令

    \b
    使用示例：csp ocr ocr-fixed-file -i '图片路径' -o '证照类型'
    """
    from csp.thirdparty import Ocr
    ocrclient = Ocr(version=version, port=port, c_name=c_name, reload=r)
    result = ocrclient.ocr_fixed_file(code, file)
    print(result)


if __name__ == '__main__':
    print("start")
    ocr()
    # name = "yrocr-cpu"
    # version = 1.2
    # port = 28888
    # img_path = "/Users/liny/work/ocr/text.png";
    # ocr_text(version, port, name, True, img_path);
