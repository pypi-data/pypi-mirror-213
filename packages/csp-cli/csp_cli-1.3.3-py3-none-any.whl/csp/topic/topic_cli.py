#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/27 9:29
# @Author  : xgy
# @Site    : 
# @File    : model_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import stat
# import subprocess
# import sys

import click
from csp.command.cli import csptools
from csp.common.utils import make_tmp


# 一级命令 CSPtools topic
@csptools.group("topic")
def topic():
    """
    业务模型镜像命令，包括业务模型镜像信息列表、上传、下载等子命令

    \b
    csp topic 'commands' -h 获取子命令使用帮助
    """


## 模型信息列表展示
@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", default=None)
@click.option("-c", "--classify", type=click.STRING, help="分类名称，根据分类名称查询，支持模型查询", default=None, show_default=True)
@click.option("-d", "--dataset", type=click.STRING, help="数据集名称，查询当前用户在某一数据集下的业务模型评估情况", default=None, show_default=True)
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
def list(name, classify, dataset, more):
    """
    业务模型镜像列表命令；查询当前用户下指定数据集的评分信息命令（需登录）

    \b
    使用示例：csp topic list or csp topic list -c "分类名称" -n "镜像资源库:镜像tag" or csp topic list -d "数据集名称"
    """
    try:
        from csp.topic.topic_server import topic_list
        if dataset:
            res = topic_list(dataset=dataset, show=more, interface_name="topic")
        else:
            res = topic_list(model_repository=name, classify=classify, show=more, interface_name="topic")
        if more:
            tmp_dir, code = make_tmp()
            os.makedirs(tmp_dir, exist_ok=True)
            txt_path = os.path.join(tmp_dir, "topic_l.txt")
            with open(txt_path, "w", encoding=code) as fw:
                fw.write(res)
            txt_abs = os.path.abspath(txt_path)
            os.chmod(txt_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.system("more " + txt_abs)

    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
@click.option("-s", "--model_source", type=click.Choice(["cloud", "local"]), help="镜像来源，local-本地；cloud-云端", prompt="镜像来源，local-本地 cloud-云端", required=True)
@click.option("-d", "--dataset", type=click.STRING, help="模型关联数据集名称", default='')
def upload(name, model_source, dataset):
    """
    业务模型镜像上传命令

    \b
    使用示例：csp topic upload -n "镜像资源库:镜像tag" -s "镜像来源(cloud/local)" -d "模型关联数据集名称(可不传为空)"
    """
    if not dataset:
        dataset = None
    try:
        from csp.topic.topic_server import topic_upload
        topic_upload(model_repository=name, model_type="topic", model_source=model_source, dataset=dataset)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
def download(name):
    """
    业务模型镜像下载命令

    \b
    使用示例：csp topic download -n "镜像资源库:镜像tag"
    """
    try:
        from csp.topic.topic_server import topic_download
        topic_download(name)
        print("镜像下载成功")
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
def info(name):
    """
    业务模型镜像评估详情命令

    \b
    使用示例：csp topic info -n "镜像资源库:镜像tag"
    """
    try:
        from csp.topic.topic_server import topic_info
        topic_info(name)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="模糊搜索查找，搜索范围包括：分类、模型名称、数据集", prompt="模糊搜索查找，搜索范围包括：分类、模型名称、数据集", required=True)
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
def find(name, more):
    """
    业务模型镜像模糊查找命令

    \b
    使用示例：csp topic find -n "安监"
    """
    try:
        from csp.topic.topic_server import topic_find
        res = topic_find(name, show=more)
        if more:
            tmp_dir, code = make_tmp()
            os.makedirs(tmp_dir, exist_ok=True)
            txt_path = os.path.join(tmp_dir, "searchfuzzy_l.txt")
            with open(txt_path, "w", encoding=code) as fw:
                fw.write(res)
            txt_abs = os.path.abspath(txt_path)
            os.chmod(txt_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.system("more " + txt_abs)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


# @topic.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称，支持模糊查找", required=True)
# def start(name):
#     """
#     模型服务启动命令
#
#     \b
#     使用示例：csp topic start
#     """
#     from csp.topic.topic_server import model_start
#     model_start(name)


# @topic.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称，支持模糊查找", required=True)
# def eva(name):
#     """
#     模型评估命令
#
#     \b
#     使用示例：csp topic eva
#     """
#     from csp.topic.topic_server import model_eva
#     model_eva()


if __name__ == '__main__':
    print("start")
