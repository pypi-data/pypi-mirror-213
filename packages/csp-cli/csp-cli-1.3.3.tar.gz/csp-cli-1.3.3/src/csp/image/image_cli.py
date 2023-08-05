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


# 一级命令 CSPtools image
@csptools.group("image")
def image():
    """
    通用镜像命令，包括通用镜像信息列表、下载、上传等子命令

    \b
    csp image 'commands' -h 获取子命令使用帮助
    """


## 模型信息列表展示
@image.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称:版本", default=None)
# @click.option("-c", "--classify", type=click.STRING, help="分类名称，根据分类名称查询，支持模型查询", default=None, show_default=True)
# @click.option("-d", "--dataset", type=click.STRING, help="数据集名称，查询当前用户在某一数据集下的业务模型评估情况", default=None, show_default=True)
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
# def list(name, classify, dataset, more):
def list(more):
    """
    通用镜像列表查询命令

    \b
    使用示例：csp image list
    """
    try:
        from csp.topic.topic_server import topic_list
        # if dataset:
        #     res = topic_list(dataset=dataset, show=more)
        # else:
        #     res = topic_list(model_repository=name, classify=classify, show=more)
        res = topic_list(model_repository=None, classify=None, show=more, interface_name="image")
        if more:
            tmp_dir, code = make_tmp()
            os.makedirs(tmp_dir, exist_ok=True)
            txt_path = os.path.join(tmp_dir, "image_l.txt")
            with open(txt_path, "w", encoding=code) as fw:
                fw.write(res)
            txt_abs = os.path.abspath(txt_path)
            os.chmod(txt_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.system("more " + txt_abs)

    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@image.command()
@click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
@click.option("-c", "--image_domain", type=click.Choice(["训练", "推理"]), help="镜像服务类型", prompt="镜像服务类型", required=True, show_default=True)
@click.option("-t", "--classify", type=click.Choice(["命名实体识别", "文本实体关系抽取", "文本分类", "图像分类", "目标检测", "关键点检测", "人体检测", "文本识别"]), help="镜像任务类型", prompt="镜像任务类型", required=True)
@click.option("-s", "--image_source", type=click.Choice(["cloud", "local"]), help="镜像来源，local-本地；cloud-云端", prompt="镜像来源，local-本地 cloud-云端", required=True)
def upload(name, image_domain, classify, image_source):
    """
    通用镜像上传命令

    \b
    使用示例：csp topic upload -n "镜像资源库:镜像tag" -c "镜像服务类型(训练/推理)" -t "镜像任务类型" -s "镜像来源(cloud/local)"
    """
    try:
        from csp.topic.topic_server import topic_upload
        topic_upload(name, image_domain=image_domain, image_classify=classify, model_type="image", model_source=image_source)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


@image.command()
@click.option("-n", "--name", type=click.STRING, help="镜像名称:版本", prompt="镜像名称:版本", required=True)
def download(name):
    """
    通用镜像下载命令

    \b
    使用示例：csp topic download -n "镜像资源库:镜像tag"
    """
    try:
        from csp.topic.topic_server import topic_download
        topic_download(name)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


# @image.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称:版本", prompt="模型名称:版本", required=True)
# def info(name):
#     """
#     通用镜像评估详情命令
#
#     \b
#     使用示例：csp topic info -n "镜像资源库:镜像tag"
#     """
#     try:
#         from csp.topic.topic_server import topic_info
#         topic_info(name)
#     except KeyError as ke:
#         print("KeyError: ", str(ke))
#     except Exception as ae:
#         print(str(ae))



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
