#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/6 15:35
# @Author  : xgy
# @Site    : 
# @File    : Detection.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os

import csp.aip.Detection
from csp.common.docker_server import DockerServer

import threading


class Detection:
    # 镜像版本号，默认值
    def_version = "1.0.6"
    # 镜像容器端口，默认值
    def_port = "30004"
    # 镜像名称，默认值
    def_name = "sec-item-detect"

    def __init__(self, mount_dir, shm_size: int, version=None, port=None, name=None, c_name=None, reload=True, gpus=None):
        self.gpus = gpus
        self.shm_size = shm_size
        self.mount_dir = mount_dir
        if version:
            self.version = version
        else:
            self.version = self.def_version
        if port:
            self.port = port
        else:
            self.port = self.def_port
        if name:
            self.name = name
        else:
            self.name = self.def_name
        if not mount_dir or not shm_size:
            raise Exception('mount_dir and shm_size are required')
        else:
            self.c_param = "--shm-size " + str(self.shm_size) + "g" + " -v " + self.mount_dir + ":" + "/data"
        self.c_name = c_name

        self.http_sdk = csp.aip.Detection(ip="127.0.0.1", port=self.port)

        # self.port = port
        self.server = DockerServer(name=self.name, version=self.version, port=self.port, c_name=c_name, c_param=self.c_param, reload=reload, gpus=self.gpus)
        self.server.start()

    def train(self, datapath, ep, bs):
        """
        模型训练
        """
        t_logs = threading.Thread(target=self.docker_log, args=(), name="train-logs")
        t_logs.start()  # 开始线程
        result = self.http_sdk.train(datapath, ep, bs)
        print(result)
        print("训练完成, ‘Ctrl+c’ 退出")

        return result

    def predict(self, datapath, bs, pretrained=False):
        """
        模型预测
        """
        t_logs = threading.Thread(target=self.docker_log, args=(), name="predict-logs")
        t_logs.start()  # 开始线程
        result = self.http_sdk.predict(datapath, bs, pretrained)
        print(result)
        print("预测完成, ‘Ctrl+c’ 退出")

        return result

    def transform(self):
        """
        模型转换
        """
        t_logs = threading.Thread(target=self.docker_log, args=(), name="transform-logs")
        t_logs.start()  # 开始线程
        result = self.http_sdk.transform()
        print(result)
        print("转换完成, ‘Ctrl+c’ 退出")

        return result

    def docker_log(self):
        if self.c_name:
            os.system("docker logs -tf " + self.c_name)
        else:
            os.system("docker logs -tf " + self.name + "-v" + str(self.version))

    def rm(self):
        self.server.rm()


if __name__ == '__main__':
    print("start")
