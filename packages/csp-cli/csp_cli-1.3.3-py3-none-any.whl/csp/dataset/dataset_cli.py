#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/18 9:44
# @Author  : xgy
# @Site    : 
# @File    : dataset_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
# import os
# import sys

import click
from csp.command.cli import csptools
from csp.dataset.dataset_server import data_download, data_get


# 一级命令 CSPtools dataset
@csptools.group("dataset")
def dataset():
    """
    数据集命令，包括数据集信息列表、数据集下载等子命令

    \b
    csp dataset 'commands' -h 获取子命令使用帮助
    """


## 数据集资源展示
@dataset.command()
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
def list(more):
    """
    数据集列表命令

    \b
    使用示例：csp dataset list
    """
    try:
        res = data_get(infer_type="list", show=more)
    except Exception as ae:
        print(ae)


## 数据集资源按名称查找
@dataset.command()
@click.option("-n", "--name", prompt="请输入数据集名称或分类名称或标注分类名称，支持模糊查询", help="数据集名称或分类名称或标注分类名称，支持模糊查询", required=True)
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
def find(name, more):
    """
    数据集查找命令

    \b
    使用示例：csp dataset find -n '数据集名称或分类名称或标注分类名称'
    """
    try:
        data_get(name, infer_type="search", show=more)
    except Exception as ae:
        print(ae)


## 数据集资源按名称展示详细信息
# @dataset.command()
# @click.option("-n", "--name", prompt="数据集名称", help="数据集名称", required=True)
# def info(name):
#     """
#     数据集信息详情查询命令
#
#     \b
#     使用示例：csp dataset info -n '数据集名称'
#     """
#     data_get(name, infer_type="info")


## 数据集资源下载
@dataset.command()
@click.option("-n", "--name", help="数据集名称", prompt="数据集名称", required=True)
@click.option("-m", "--mode", type=click.Choice(['raw', 'train', 'eval']),
              prompt="数据类型，须选择其一", help="数据类型，须选择其一。raw：原始数据，train：训练数据，eval：验证数据", required=True)
@click.option("-s", "--size", type=click.INT, help="下载文件数量，默认0即下载全部", prompt="下载文件数量，默认0即下载全部", default=0, show_default=True)
@click.option("-o", "--output", help="数据集保存路径", prompt="数据集保存路径", required=True)
def download(name, mode, size, output):
    """
    数据集下载命令

    \b
    使用示例：csp dataset download -n '数据集名称' -m '数据类型' -s '欲下载文件数量' -o '数据集保存路径'
    """
    try:
        if size:
            if size < 0:
                raise TypeError("-s/--size下载文件数量 必须是正整数")
        else:
            size = None
        save_path = data_download(name, mode, size, output)
        print("数据集已保存至 {}".format(save_path))
    except FileNotFoundError as fe:
        print("error: ", fe)
    except Exception as ae:
        print(ae)


if __name__ == '__main__':
    print("start")
