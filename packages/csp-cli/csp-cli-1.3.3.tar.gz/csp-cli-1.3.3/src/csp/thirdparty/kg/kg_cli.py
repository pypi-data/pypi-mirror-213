#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/28 17:30
# @Author  : xgy
# @Site    : 
# @File    : kg_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click

from csp.command.cli import csptools
from csp.common.utils import format
# from csp.thirdparty import Kg


# 一级命令 CSPtools kg
@csptools.group("kg")
def kg():
    """
    知识图谱页面展示命令，包括图谱创建、列表、删除等子命令

    \b
    csp kg 'commands' -h 获取子命令使用帮助
    """


## 创建图谱
@kg.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-d", "--class_file", help="本体设计csv文件路径", required=True)
@click.option("-l", "--link_file", help="关系数据csv文件路径", required=True)
@click.option("-e", "--node_file", help="实体数据csv文件路径", required=True)
@click.option("-i", "--code", help="图谱唯一编码", required=True)
@click.option("-n", "--name", help="图谱名称", required=True)
def create(version, port, c_name, r, class_file, link_file, node_file, code, name):
    """
    知识图谱创建命令

    \b
    执行成功后，可根据提示打开网页

    \b
    使用示例：csp kg create -d '本体设计csv文件' -l '关系数据csv文件' -e '实体数据csv文件' -i '图谱唯一编码' -n '图谱名称'
    """
    from csp.thirdparty import Kg
    kg = Kg(version=version, port=port, c_name=c_name, reload=r)
    result = kg.create(class_file, code, link_file, name, node_file)


# 图谱列表
@kg.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
def list(version, port, c_name, r):
    """
    知识图谱列表命令

    \b
    必须在知识图谱创建命令执行成功后使用，否则为空

    \b
    使用示例：csp kg list
    """
    from csp.thirdparty import Kg
    kg = Kg(version=version, port=port, c_name=c_name, reload=r)
    result = kg.list()
    title_dict = {"id": "id", "图谱名称": 'kgName', "图谱标识符": 'kgCode', "图谱描述": 'kgDesc', "创建者": 'creator',
                  "创建时间": "createTime"}
    print("kg ui url at {}".format(result["url"]))
    res_dict = {"data": result['records']}
    format(res_dict, title_dict)


# 图谱删除
@kg.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--code", help="图谱唯一编码", required=True)
def delete(version, port, c_name, r, code):
    """
    知识图谱删除命令

    \b
    按图谱唯一编码删除图谱

    \b
    使用示例：csp kg delete -i '图谱唯一编码'
    """
    from csp.thirdparty import Kg
    kg = Kg(version=version, port=port, c_name=c_name, reload=r)
    result = kg.delete(code)


if __name__ == '__main__':
    print("start")
