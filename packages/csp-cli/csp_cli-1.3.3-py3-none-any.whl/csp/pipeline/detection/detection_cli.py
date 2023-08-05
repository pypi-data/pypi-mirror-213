#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/9 11:13
# @Author  : xgy
# @Site    : 
# @File    : detection_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
import os
from csp.pipeline.pipeline_cli import pipeline


@pipeline.group("detection")
def detection():
    """
    目标检测模型流水线框架命令，包括训练、预测、转换等子命令

    \b
    csp pipeline detection 'commands' -h 获取子命令使用帮助
    """


@detection.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("--datapath", '-d', help="训练数据目录", type=str, required=True)
@click.option("--ep", '-e', help="训练 epoch", default=150, type=int, show_default=True)
@click.option("--bs", '-b', help="训练 batch size", default=32, type=int, show_default=True)
@click.option("--shm_size", '-s', help="共享内存 (G)", default=16, type=int, show_default=True)
@click.option("--gpus", '-g', help="GPU编号，默认为'all'，即使用所有GPU", default='all', show_default=True)
def train(datapath, ep, bs, shm_size, gpus, version, port, c_name, r):
    """
    模型训练命令

    \b
    使用示例：csp pipeline detection train -d '训练数据集目录' -e 10 -b 16 -s 16
    """
    from csp.pipeline import Detection
    # mount_dir = os.path.abspath(datapath)
    mount_dir = os.path.abspath(os.path.dirname(datapath))
    det = Detection(version=version, port=port, c_name=c_name, reload=r, mount_dir=mount_dir, shm_size=shm_size, gpus=gpus)
    train_dataset = os.path.basename(datapath)
    ep = ep
    bs = bs
    model_train = det.train(train_dataset, ep, bs)
    # detection = Detection(mount_dir=mount_dir, shm_size=shm_size, gpus=gpus)


@detection.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("--datapath", '-d', help="待预测图片文件夹", type=str, required=True)
@click.option('-m', is_flag=True, default=False, help="标识符，出现则使用内置的安监模型作模型预测")
@click.option("--bs", '-b', help="预测 batch size", default=32, type=int, show_default=True)
@click.option("--shm_size", '-s', help="共享内存 (G)", default=16, type=int, show_default=True)
@click.option("--gpus", '-g', help="GPU编号，默认为'all'，即使用所有GPU", default='all', show_default=True)
def predict(datapath, bs, shm_size, gpus, version, port, c_name, r, m):
    """
    模型预测命令

    \b
    使用示例：csp pipeline detection predict -d '待预测图片数据集目录' -b 16 -s 16
    """
    from csp.pipeline import Detection
    # mount_dir = os.path.abspath(datapath)
    mount_dir = os.path.abspath(os.path.dirname(datapath))
    det = Detection(version=version, port=port, c_name=c_name, reload=r, mount_dir=mount_dir, shm_size=shm_size, gpus=gpus)
    predict_dataset = os.path.basename(datapath)
    bs = bs
    model_predict = det.predict(predict_dataset, bs, m)


@detection.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("--datapath", '-d', help="训练数据集目录", type=str, required=True)
@click.option("--shm_size", '-s', help="共享内存 (G)", default=16, type=int, show_default=True)
@click.option("--gpus", '-g', help="GPU编号，默认为'all'，即使用所有GPU", default='all', show_default=True)
def transform(datapath, shm_size, gpus, version, port, c_name, r):
    """
    模型转换命令

    \b
    此命令必须在模型训练命令执行成功后才能正确执行

    \b
    使用示例：csp pipeline detection transform -d '训练数据集目录' -s 16
    """
    from csp.pipeline import Detection
    mount_dir = os.path.abspath(os.path.dirname(datapath))
    # mount_dir = os.path.abspath(datapath)
    det = Detection(version=version, port=port, c_name=c_name, reload=r, mount_dir=mount_dir, shm_size=shm_size, gpus=gpus)
    model_transform = det.transform()
    # print("转换完成", model_transform)


@detection.command()
@click.option("-v", "--version", help="容器服务的镜像版本", default="1.0.6", show_default=True)
@click.option("-c", "--c_name", help="容器名，默认为内置的容器名，一般不传即可", default=None)
def rm(version, c_name):
    """
    容器服务删除命令

    \b
    使用示例：csp pipeline detection rm -v '容器版本号' -c '容器名'
    """
    if c_name:
        container_name = c_name
    else:
        container_name = "sec-item-detect-v" + version
    try:
        rm_cmd = "docker rm -f " + container_name
        os.system(rm_cmd)
    except Exception as re:
        raise Exception("容器删除失败：" + repr(re))


if __name__ == '__main__':
    print("start")
