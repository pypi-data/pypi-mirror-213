#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/6 17:30
# @Author  : xgy
# @Site    : 
# @File    : Detection.py
# @Software: PyCharm
# @python version: 3.7.4
"""

from .common.http_client import HttpClient


class Detection:
    # 镜像版本号，默认值
    def_version = "1.0.6"
    # 镜像容器端口，默认值
    def_port = "30004"
    # 镜像名称，默认值
    def_name = "sec-item-detect"

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def train(self, datapath, ep=150, bs=32):
        """
        训练接口
        """
        http_client = HttpClient()
        url = "http://" + self.ip + ":" + str(self.port) + "/model_train"
        data = {
            "datapath": datapath,
            "ep": ep,
            "bs": bs
        }
        print("发送训练指令")
        dt = http_client.post(url, arg_type="data", **data)
        return dt

    def predict(self, datapath, bs=32, pretrained=False):
        """
        训练接口
        """
        http_client = HttpClient()
        url = "http://" + self.ip + ":" + str(self.port) + "/sec_item"
        data = {
            "datapath": datapath,
            "pretrained": pretrained,
            "bs": bs,
        }
        print("发送预测指令")
        dt = http_client.post(url, arg_type="data", **data)
        return dt

    def transform(self):
        """
        转换接口
        """
        http_client = HttpClient()
        url = "http://" + self.ip + ":" + str(self.port) + "/model_transfer"
        print("发送转换指令")
        dt = http_client.post(url)
        return dt


if __name__ == '__main__':
    print("start")
