#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/18 18:08
# @Author  : xgy
# @Site    : 
# @File    : resource_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
from csp.command.cli import csptools
from csp.resource.resource_server import res_get, res_download


# 一级命令 CSPtools resource
@csptools.group("resource")
def resource():
    """
    资源命令，包括资源信息列表、资源下载等子命令

    \b
    csp resource 'commands' -h 获取子命令使用帮助
    """


## 资源列表查看
@resource.command()
@click.option("-n", "--name", help="资源名称/目录名称，不传则默认展示一级资源目录", default=None)
def list(name):
    """
    资源列表命令

    \b
    使用示例：csp resource list -n '资源名称/目录名称'
    """
    try:
        res_get(name=name, infer_type="list")
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


## 资源查找
@resource.command()
@click.option("-n", "--name", help="资源名称", default=None)
@click.option("-r", "--resdir", help="资源目录", default=None)
def find(name, resdir):
    """
    资源查找命令

    \b
    按资源名称（-n）或资源目录（-r）查找，或同时按名称、目录查找

    \b
    使用示例：csp resource find -n '数据集名称'
    """
    if not name and not resdir:
        raise NameError("-n/--name -r/--resdir 应至少存在一个")
    try:
        res_get(name=name, res_dir=resdir, infer_type="search")
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


## 资源详细信息查看
# @resource.command()
# @click.option("-n", "--name", help="资源名称，必须为完整名称", required=True)
# def info(name):
#     """
#     资源信息详情查询命令
#
#     \b
#     使用示例：csp resource info -n '资源名称'
#     """
#     try:
#         res_get(name=name, infer_type="info")
#     except KeyError as ke:
#         print("KeyError: ", str(ke))
#     except Exception as ae:
#         print(str(ae))


## 资源下载
@resource.command()
@click.option("-n", "--name", help="资源名称", prompt="资源名称", required=True)
@click.option("-c", "--charset", help="资源编码，一般不传即可", default="UTF-8", show_default=True)
@click.option("-o", "--output", help="保存目录", prompt="保存目录", required=True)
def download(name, charset, output):
    """
    资源下载命令

    \b
    使用示例：csp resource download -n '资源名称' -o "保存目录"
    """
    try:
        save_path = res_download(name, output, charset)
        print("资源已保存至 {}".format(save_path))
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


if __name__ == '__main__':
    print("start")
