#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/17 17:34
# @Author  : xgy
# @Site    : 
# @File    : http_client.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import getpass
import os
# import sys
import time
import urllib

import requests
import json
# from loguru import logger
from tqdm import tqdm


class HttpClient:

    def __init__(self):

        self.info_list = None
        self.info_download = None

    def get(self, url, **kw):
        params = kw
        res = requests.get(url, params=params)
        res_dict = json.loads(res.text)
        if res_dict["code"] == 200:
            self.info_list = res_dict
            return res_dict
        else:
            # raise IOError(self.error_msg(res_dict))
            self.error_msg(res_dict)
        # return res_dict

    def post(self, url, arg_type=None, **kw):
        if arg_type == "files":
            res = requests.post(url, files=kw)
        elif arg_type == "data":
            res = requests.post(url, data=kw)
        elif arg_type == "json":
            res = requests.post(url, json=kw)
        elif arg_type == "data/files":
            # 同时传文件和参数
            res = requests.post(url, files=kw["files"], data=kw["data"])
        elif arg_type is None:
            res = requests.post(url)
        else:
            raise KeyError("the arg_type for post should be in {}".format(['files', 'data', 'json', 'data/files']))

        status_code = res.status_code

        if status_code != 200:
            raise ConnectionError("服务端http调用失败，状态非200")
        else:
            res_dict = json.loads(res.text)
            if res_dict["code"] == 200:
                self.info_list = res_dict
                return res_dict
            else:
                res = self.error_msg(res_dict)
                raise ConnectionError("error_code:{}，message:{}".format(res[0], res[1]))

    def download(self, url, output=None, header=None, **kw):
        kw = kw
        if header:
            res = requests.post(url, headers=header, data=kw, stream=True)
        else:
            res = requests.post(url, data=kw, stream=True)

        status_code = res.status_code

        if status_code != 200:
            try:
                res_dict = json.loads(res.text)
            except Exception as ae:
                print("error! {}".format(res.text))
                raise ConnectionError("服务器链接失败！{}".format(ae))
            try:
                msg = res_dict["msg"]
            except Exception as e1:
                msg = res_dict["message"]
            if msg == "Invalid access token":
                # raise ValueError("token 无效，请登录 csp user login")
                print("token无效，下载失败，请登录，重新下载。登录命令：csp user login (没有账号？使用csp user register 注册一个吧)")
                # 跳转至登录
                from csp.login import login
                user_name = input("用户名：")
                passwd = getpass.getpass("密码：")
                user_data = login(user_name, passwd)
                user_token = user_data["access_token"]
                header = {"Authorization": "Bearer " + user_token}
                time.sleep(1)
                print("登录成功，重新下载中。。。")
                result = self.download(url, output=output, header=header, **kw)
                return result

            # 数据集存在性检验
            if str(status_code) == '701':
                # raise Exception(json.loads(res.text))
                raise FileNotFoundError("请求的资源不存在")
            error_res = self.error_msg(res_dict)
            if error_res:
                raise ConnectionError("error_code:{}，message:{}".format(error_res[0], error_res[1]))
        else:
            total = int(res.headers.get('content-length', 0))
            # 获取头部信息
            disposition = str(res.headers.get('Content-Disposition'))
            # 截取头部信息文件名称
            filename = disposition.replace('attachment;filename=', '')

            # 转码
            filename = urllib.parse.unquote(filename)
            save_path = os.path.join(output, filename)

            # 添加保存路径
            with open(save_path, 'wb') as file, tqdm(desc=save_path, total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
                for data in res.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            return save_path

    def error_msg(self, data):
        if data["code"] != 200:
            # print(data)
            error_code = data["code"]
            try:
                # logger.error("error_code:{},message:{}", error_code, data["message"])
                return [error_code, data["message"]]
            except Exception as ce:
                # logger.error("error_code:{},message:{}", error_code, data["msg"])
                return [error_code, data["msg"]]

    # def convert(self, url, method, arg_type, **kwargs):
    #     if method.upper() == "POST":
    #         if arg_type == "files":
    #             res = requests.post(url, files=kwargs)
    #         elif arg_type == "data":
    #             res = requests.post(url, data=kwargs)
    #         elif arg_type == "json":
    #             res = requests.post(url, json=kwargs)
    #         else:
    #             raise KeyError("the arg_type for post should be in {}".format(['files', 'data', 'json']))
    #     elif method.upper() == "GET":
    #         res = requests.get(url, params=kwargs)
    #     else:
    #         raise KeyError("the HTTP method should be POST or GET")
    #     res_dict = json.loads(res.text)
    #     self.error_msg(res_dict)
    #
    #     return res_dict


if __name__ == '__main__':
    print("start")
