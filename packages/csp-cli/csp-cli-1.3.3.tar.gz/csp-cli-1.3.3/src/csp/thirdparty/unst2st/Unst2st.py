#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/19 17:55
# @Author  : xgy
# @Site    : 
# @File    : Unst2st.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import csp.aip.Unst2st
from csp.common.docker_server import DockerServer
# from csp.common.http_client import HttpClient
from csp.aip.common.http_client import HttpClient


class Unst2st:
    # 镜像版本号，默认值
    def_version = "0.3.6"
    # 镜像容器端口，默认值
    def_port = "9889"
    # 镜像名称，默认值
    def_name = "unst2st"

    def __init__(self, version=None, port=None, c_name=None, name=None, reload=True):
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

        self.http_sdk = csp.aip.Unst2st(ip="127.0.0.1", port=self.port)

        self.server = DockerServer(name=self.name, version=self.version, port=self.port, c_name=c_name, reload=reload)
        self.server.start()

    def extract_text(self, file, output=None):
        """
        文档转纯文本
        """
        result = self.http_sdk.extract_text(file, output)

        return result

    def remove_watermark(self, file, output):
        """
        pdf 去水印
        """
        result = self.http_sdk.remove_watermark(file, output)

        return result

    def extract_img_txt(self, file, output=None):
        """
        图片内容提取
        :param file: 文件路径
        :param output: 结果输出
        :return:
        """
        result = self.http_sdk.extract_img_txt(file, output)

        return result

    def extract_table(self, file, output=None):
        """
        表格提取
        :param file: 文件路径
        :param output: 结果输出
        :return:
        """
        result = self.http_sdk.extract_table(file, output)

        return result

    def extract_structure(self, file, output=None):
        """
        篇章段落抽取
        :param file: 文件路径
        :param output: 结果输出
        :return:
        """
        result = self.http_sdk.extract_structure(file, output)

        return result


if __name__ == '__main__':
    print("start")
