#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/16 11:11
# @Author  : xgy
# @Site    : 
# @File    : resource_server.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os

from csp.aip.common.http_client import HttpClient
from csp.common.config import Configure
from csp.common.utils import format
from csp.login import check_user


def res_get(name, res_dir=None, infer_type: str = None, config: Configure = None):
    assert infer_type in ["search", "list", "info"]

    if config:
        interface_config = config.data
    else:
        interface_config = Configure().data
    http_client = HttpClient()

    url = interface_config[infer_type]["resource"]
    if infer_type == "list":
        params = {"name": name}
    elif infer_type == "search":
        params = {"resName": name, "resDir": res_dir}
    elif infer_type == "info":
        params = {"name": name}
    else:
        raise KeyError("infer_type should be in {}".format(["search", "list", "info"]))

    res_dict = http_client.get(url, **params)

    if infer_type == "list" or infer_type == "search":
        title_dict = {"名称": "resName", "文件类型": "fileType", "目录": "resDir", "资源大小(KB)": "fileSize",
                      "资源描述": "resDesc", "创建时间": "createTime"}
        format(res_dict, title_dict)

    if infer_type == "info":
        # title_dict = {"名称": "resName", "文件类型": "fileType", "目录": "resDir", "资源大小(KB)": "fileSize",
        #               "创建时间": "createTime", "更新时间": "updateTime", "描述": "resDesc"}
        # format(res_dict, title_dict)

        info_dict = {"名称": res_dict["data"]["resName"],
                     "资源描述": res_dict["data"]["resDesc"]}
        json_data = json.dumps(info_dict, ensure_ascii=False, indent=4)
        print(json_data)

    return res_dict


def res_download(name, output, charset="UTF-8"):
    interface_config = Configure().data
    http_client = HttpClient()

    user_data = check_user()
    user_token = user_data["access_token"]

    os.makedirs(output, exist_ok=True)

    header = {"Authorization": "Bearer " + user_token}

    url = interface_config["download"]["resource"]
    params = {"name": name, "charset": charset}
    print("正在请求下载，请稍等。。。。。。")
    save_path = http_client.download(url, output, header, **params)

    return save_path


if __name__ == '__main__':
    print("start")
