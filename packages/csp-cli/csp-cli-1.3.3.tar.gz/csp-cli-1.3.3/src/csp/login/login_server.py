#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/11/16 11:28
# @Author  : xgy
# @Site    : 
# @File    : login_server.py
# @Software: PyCharm
# @python version: 3.7.13
"""
import json
import os
import time
import getpass

import yaml
from csp.common.config import Configure
from csp.aip.common.http_client import HttpClient
import requests

"""
登录操作支持单用户
"""


parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
user_file = os.path.join(parent_path, "common/config", "user_config.yaml")


def user_login(username, passwd):
    # 调用后端登录服务
    infer_dict = Configure().data
    get_token_url = infer_dict["user"]["token"]
    client_id = infer_dict["user"]["clientId"]
    client_secret = infer_dict["user"]["clientSecret"]

    params = {"clientId": client_id, "clientSecret": client_secret, "username": username, "password": passwd}
    http_client = HttpClient()
    res = http_client.post(get_token_url, arg_type="data", **params)

    user_data = {"username": username, "access_token": res['data']['access_token']}

    with open(user_file, "w", encoding="utf-8") as fw:
        yaml.dump(user_data, fw)
    return user_data


def user_logout():
    if not os.path.exists(user_file):
        print("登出成功")
    else:
        infer_dict = Configure().data
        logout_url = infer_dict["user"]["logout"]
        user_data = Configure(user_file).data
        user_token = user_data["access_token"]
        header = {"Authorization": "Bearer " + user_token}
        params = {"access_token": user_token}
        res = requests.get(logout_url, headers=header, params=params)
        res_dict = json.loads(res.text)

        try:
            msg = res_dict["msg"]
        except KeyError as ke:
            msg = res_dict["message"]
        # 服务端返回token过期信息
        if msg == "Invalid access token":
            os.remove(user_file)
            print("登出成功")
        elif msg == "退出登录成功！":
            os.remove(user_file)
            print("登出成功")
        else:
            raise RuntimeError("退出登录错误")


def check_user():
    if not os.path.exists(user_file):
        print("请先登录 csp user login")
        user_name = input("用户名：")
        passwd = getpass.getpass("密码：")
        user_login(user_name, passwd)
        time.sleep(1)
        print("登录成功")
        user_data = Configure(user_file).data
        return user_data
    else:
        user_data = Configure(user_file).data
        return user_data


def re_login(fc, **kw):
    user_name = input("用户名：")
    passwd = getpass.getpass("密码：")
    user_login(user_name, passwd)
    time.sleep(1)
    print("登录成功")
    res = fc(**kw)
    return res


def user_register(username, passwd, nickname):
    # 调用后端注册服务
    infer_dict = Configure().data
    register_url = infer_dict["user"]["register"]

    params = {"fullName": nickname, "userName": username, "password": passwd}
    http_client = HttpClient()
    res = http_client.post(register_url, arg_type="data", **params)
    try:
        msg = res["msg"]
    except Exception:
        msg = res["message"]
    if msg == "用户注册成功":
        print("注册成功，等待管理员审核")
    else:
        raise ConnectionError("error_code:{}，message:{}".format(res["code"], msg))

    return res


if __name__ == '__main__':
    print("start")
