#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/18 9:53
# @Author  : xgy
# @Site    : 
# @File    : dataset_server.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os
import stat
import subprocess

# from csp.common.http_client import HttpClient
import sys

from csp.aip.common.http_client import HttpClient
from csp.common.config import Configure
from csp.common.utils import format, make_tmp
from csp.login import check_user


# from datetime import datetime


def data_list(name=None):
    interface_config = Configure().data
    http_client = HttpClient()

    url = interface_config["search"]["dataset"]
    params = {"name": name}
    res_dict = http_client.get(url, **params)

    # title_dict = {"名称": "name", "分类": "classify", "标注分类": "annotationType", "源数据": "rawDataNum", "训练数据": "trainDataNum", "验证数据": "evaDataNum",
    #               "创建时间": "createTime", "更新时间": "updateTime", "描述": "funDesc"}

    title_dict = {"名称": "name", "分类": "classify", "标注分类": "annotationType", "原始数据": "rawDataNum", "训练数据": "trainDataNum", "验证数据": "evaDataNum",
                  "功能描述": "funDesc"}

    format(res_dict, title_dict)


def data_get(name=None, infer_type: str = None, show=True):
    interface_config = Configure().data
    http_client = HttpClient()

    url = interface_config["search"]["dataset"]
    params = {"name": name}
    res_dict = http_client.get(url, **params)

    if infer_type == "list" or infer_type == "search":
        title_dict = {"名称": "name", "分类": "classify", "标注分类": "annotationType", "原始数据": "rawDataNum", "标注数据": "trainDataNum",
                      "验证数据": "evaDataNum", "功能描述": "funDesc"}

        string = format(res_dict, title_dict, show=show)

        if show:
            tmp_dir, code = make_tmp()
            os.makedirs(tmp_dir, exist_ok=True)
            txt_path = os.path.join(tmp_dir, "dataset_l.txt")

            with open(txt_path, "w", encoding=code) as fw:
                fw.write(repr(string))
            os.chmod(txt_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            txt_abs = os.path.abspath(txt_path)
            os.system("more " + txt_abs)
            return string

    if infer_type == "info":
        info_dict = {"名称": res_dict["data"][0]["name"],
                     "分类": res_dict["data"][0]["classify"],
                     "标注分类": res_dict["data"][0]["annotationType"],
                     "原始数据": res_dict["data"][0]["rawDataNum"],
                     "标注数据": res_dict["data"][0]["trainDataNum"],
                     "验证数据": res_dict["data"][0]["evaDataNum"],
                     "创建时间": res_dict["data"][0]["createTime"],
                     "更新时间": res_dict["data"][0]["updateTime"],
                     "描述": res_dict["data"][0]["funDesc"]}
        json_data = json.dumps(info_dict, ensure_ascii=False, indent=4)
        print(json_data)


def data_download(name, mode, size, output):
    interface_config = Configure().data
    http_client = HttpClient()

    user_data = check_user()
    user_token = user_data["access_token"]

    os.makedirs(output, exist_ok=True)

    header = {"Authorization": "Bearer " + user_token}
    url = interface_config["download"]["dataset"]
    params = {"name": name, "mode": mode, "size": size}
    print("正在请求下载，请稍等。。。。。。")
    save_path = http_client.download(url, output, header, **params)

    return save_path


if __name__ == '__main__':
    print("start")
