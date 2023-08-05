#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/27 8:52
# @Author  : xgy
# @Site    : 
# @File    : model_server.py
# @Software: PyCharm
# @python version: 3.7.4
"""
# import getpass
import json
import os
# import time
# import re
from typing import Union, Any
import subprocess

import requests

from csp.aip.common.http_client import HttpClient
from csp.common.config import Configure
from csp.common.utils import format, convert_bytes, aes_decrypt
from csp.login import check_user
from csp.login.login_server import re_login


# 新版list 不再有合并单元格
def topic_list(model_repository=None, classify=None, dataset=None, interface_name=None, show=True):
    if model_repository:
        model_name, model_tag = model_repository.split(":")
    else:
        model_name, model_tag = None, None

    interface_config = Configure().data
    http_client = HttpClient()

    if dataset:
        if interface_name == "topic":
            url = interface_config["list"]["user_model"]
        else:
            raise ValueError("只在topic命令中适用")
        params = {"datasetName": dataset}
        user_data = check_user()
        user_token = user_data["access_token"]
        header = {"Authorization": "Bearer " + user_token}
        res = requests.get(headers=header, url=url, params=params)
        res_dict = json.loads(res.text)

        try:
            msg = res_dict["msg"]
        except KeyError as ke:
            msg = res_dict["message"]
        if msg == "Invalid access token":
            print(
                "token无效，查询失败，请登录，重新查询。登录命令：csp user login (没有账号？使用csp user register 注册一个吧)")
            # 跳转至登录
            result = re_login(topic_list, model_repository=model_repository, classify=classify,
                              interface_name=interface_name, dataset=dataset, show=show)
            return result

        if not res_dict["data"]:
            raise ValueError("未查到相关记录")
        try:
            scores = res_dict['data'][0]['scoresInfo']
            if not scores:
                title_dict = {"作者": "author", "数据集名称": "datasetName", "提交时间": "createTime",
                              "状态": "statusLabel"}
            else:
                classify_flag = json.loads(res_dict['data'][0]['scoresInfo'])
                if classify_flag[0].get('ap', None) or classify_flag[0].get('ap', None) == 0:
                    title_dict = {"作者": "author", "数据集名称": "datasetName", "总分": "modelScores",
                                  "召回率": "recall", "准确率": "precision", "ap": "ap", "提交时间": "createTime",
                                  "状态": "statusLabel"}
                elif classify_flag[0].get('fScore', None) or classify_flag[0].get('fScore', None) == 0:
                    title_dict = {"作者": "author", "数据集名称": "datasetName", "总分": "modelScores",
                                  "召回率": "recall", "准确率": "precision", "f1": "fScore", "提交时间": "createTime",
                                  "状态": "statusLabel"}
                elif classify_flag[0].get('imageScore', None) or classify_flag[0].get('imageScore', None) == 0:
                    title_dict = {"作者": "author", "数据集名称": "datasetName", "总分": "modelScores",
                                  "漏检率": "missingRate", "错误率": "errorRate", "正确率": "correctRate",
                                  "分数": "imageScore", "提交时间": "createTime", "状态": "statusLabel"}
                else:
                    raise KeyError('该评分类型不支持')
            res_dict_drop = []
            for item in res_dict["data"]:
                if not scores:
                    drop_item = {"author": item["author"],
                                 "datasetName": item["datasetName"],
                                 "createTime": item["createTime"],
                                 "statusLabel": item["statusLabel"]}
                else:
                    drop_item = {"author": item["author"],
                                 "datasetName": item["datasetName"],
                                 "modelScores": item["modelScores"],
                                 "createTime": item["createTime"],
                                 "statusLabel": item["statusLabel"]}
                    scoresInfo = json.loads(item["scoresInfo"])
                    if title_dict.get("ap"):
                        for score in scoresInfo:
                            if score["category"] == "total":
                                drop_item["recall"] = score["recall"]
                                drop_item["precision"] = score["precision"]
                                drop_item["ap"] = score["ap"]
                    elif title_dict.get("f1"):
                        for score in scoresInfo:
                            if score["category"] == "total":
                                drop_item["recall"] = score["recall"]
                                drop_item["precision"] = score["precision"]
                                drop_item["fScore"] = score["fScore"]
                    elif title_dict.get("分数"):
                        for score in scoresInfo:
                            if score["category"] == "total":
                                drop_item["missingRate"] = score["missingRate"]
                                drop_item["errorRate"] = score["errorRate"]
                                drop_item["correctRate"] = score["correctRate"]
                                drop_item["imageScore"] = score["imageScore"]
                    else:
                        raise KeyError('该评分类型不支持')
                res_dict_drop.append(drop_item)

            res_dict_drop = {"data": res_dict_drop}
            x = format(res_dict_drop, title_dict, show=show)
            x_string = x.get_string()
            return x_string
        except Exception as ae:
            if res_dict["data"]["scoresInfo"] is None:
                print("name: ", model_repository)
                raise ValueError("模型未评估")
            elif not res_dict["data"]["scoresInfo"]:
                print("name: ", model_repository)
                raise ValueError('评估结果为空')
            else:
                raise ae

    else:
        if interface_name == "topic":
            url = interface_config["list"]["model"]
            params = {"modelName": model_name, "classifyName": classify, "modelVersion": model_tag}
            res_dict = http_client.get(url, **params)

            title_dict = {"分类": "classifyName", "模型名称": "modelName", "版本": "modelVersion", "大小": "size",
                          "评分": "modelScores",
                          "关联数据集": "datasetName", "数据集描述": "funDesc", "作者": "author",
                          "创建时间": "createTime"}

            x = format(res_dict, title_dict, show=show)
            x_string = x.get_string()

        elif interface_name == "image":
            url = interface_config["list"]["image"]
            params = {"imagesName": model_name, "classifyName": classify, "imagesVersion": model_tag}
            res_dict = http_client.get(url, **params)

            title_dict = {"分类": "classifyName", "镜像类型": "imagesType", "模型名称": "imagesName",
                          "版本": "imagesVersion", "大小": "size"}

            x = format(res_dict, title_dict, show=show)
            x_string = x.get_string()
        else:
            raise ValueError("interface_name 取值须为topic或image")
        return x_string


# 新版上传、下载；物料 为docker 镜像，上传同时注册至服务端
def topic_upload(model_repository: str, model_type: str, model_source: str, image_domain: str = None,
                 image_classify: str = None, dataset: str = None):
    """

    Parameters
    ----------

    image_domain: 通用镜像服务分类（训练、推理）
    image_classify: 通用镜像任务领域分类（命名实体识别、文本实体关系抽取、文本分类、图像分类、目标检测、关键点检测、人体检测、文本识别）
    model_repository: 镜像名称及版本
    model_type：镜像类型（通用-image、业务-topic）
    model_source：镜像来源（本地，云端dockerhub）
    dataset: 关联数据集（业务镜像）

    Returns
    -------

    """
    if model_source not in ["cloud", "local"]:
        raise ValueError("镜像来源，local-本地 cloud-云端")
    if model_type not in ["topic", "image"]:
        raise ValueError("镜像类型，topic-业务镜像 image-通用镜像")
    user_data = check_user()
    user_token = user_data["access_token"]
    if ":" not in model_repository:
        model_name, model_tag = model_repository, "latest"
    else:
        try:
            model_name, model_tag = model_repository.split(":")
        except ValueError as VE:
            raise ValueError("镜像名称格式错误. 示例：local {}；cloud {}".format("镜像名称:版本号(kg:1.0.0)", "资源路径:版本号(ubuntu:18.04) 或 用户名/资源路径:版本号(zhys513/pytorch:1.0.0)"))
    interface_config = Configure().data

    # 上传镜像前检查服务端是否已注册
    image_url = check_image_in(model_repository)
    # image_url = False
    if image_url:
        # 是否覆盖
        # is_cover = input("镜像已存在，是否覆盖（yes/no）:")
        # while is_cover.lower() in ["yse", "y", "no", "n"]:
        #     is_cover = input("请输入正确指令（yes/no）:")
        # if is_cover.lower() == "no" or is_cover.lower() == "n":
        #     print("镜像上传已终止")
        #     return False
        # print("上传失败，已存在相同模型名称和版本的记录！")
        raise NameError("上传失败，已存在相同模型名称和版本的记录！")
    else:
        # 上传前判断镜像是否存在
        # 检查外部镜像是否存在
        image_size = None
        if model_source == "cloud":
            flag_infe_dockerhub = input("是否连接dockerhub判断镜像存在（yes/no）:")
            while flag_infe_dockerhub.lower() not in ["yes", "y", "no", "n"]:
                flag_infe_dockerhub = input("请输入正确指令（yes/no）:")
            if flag_infe_dockerhub.lower() == "yes" or flag_infe_dockerhub.lower() == "y":
                is_image_exited, image_size = check_image_out(model_name, model_tag)
                if not is_image_exited:
                    raise NameError("镜像在dockerhub不存在或未公开")
            else:
                print("不查询dockerhub，将直接上传，请确保镜像存在")
                print("因您选择了不链接dockerhub，将直接上传，请确保镜像存在，并需手动输入镜像大小（需包含单位MB或GB）")
                size_flag = True
                while size_flag:
                    image_size = input("请输入镜像大小：")
                    if len(str(image_size)) < 3:
                        print("请输入合法长度不小于3的字符(含单位)，如1MB")
                    else:
                        f, b = str(image_size)[:-2], str(image_size)[-2:]
                        if b not in ["MB", "GB"]:
                            print("请使用正确的单位（MB/GB）")
                        else:
                            try:
                                num = float(f)
                                if not num:
                                    print("镜像大小不能为0")
                                else:
                                    size_flag = False
                            except ValueError as VE:
                                print("文件大小必须为数字")

        # 检查内部镜像是否存在并上传至私服
        # out = None
        if model_source == "local":
            # 登录私服
            yek = b"kdajfkds"
            u_en_str = 'JRcSk5th9pO9hgSLD6RCsQ=='
            u_str = aes_decrypt(u_en_str, yek)
            p_en_str = 'B3vfZVtvGd/EG1LK+3FlNw=='
            p_str = aes_decrypt(p_en_str, yek)

            cmd_login_nux = 'docker login -u ' + u_str + ' -p ' + p_str + ' 27.196.43.168:28081'
            res_login = subprocess.Popen(cmd_login_nux, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out_login = res_login.stdout.read().decode("utf-8")
            # docker 服务未起或登录私服失败
            if out_login.startswith(
                    "error during connect: This error may indicate that the docker daemon is not running"):
                raise RuntimeError("docker服务未开启")
            if out_login.replace("\n", "").startswith(
                    "WARNING! Using --password via the CLI is insecure. Use --password-stdin.error during connect: This error may indicate that the docker daemon is not running"):
                raise RuntimeError("docker服务未开启")
            if out_login.replace("\n", "").endswith("http: server gave HTTP response to HTTPS client"):
                raise RuntimeError(
                    '''须配置私服地址：vim /etc/docker/daemon.json，增加字段 "insecure-registries": ["27.196.43.168:28081"]. windows系统在Docker Desktop的 Settings-Docker Engine 中配置''')
            if not out_login.rstrip("\n").endswith("Login Succeeded"):
                raise ConnectionError("私服登录失败，请检查docker私服配置是否正确，或能否连接docker私服仓库")
            # 镜像打tag，并判断本地镜像存在性
            cmd_tag = 'docker tag ' + model_repository + " " + "27.196.43.168:28081/cspdevkit/aip/" + model_repository
            res_tag = subprocess.Popen(cmd_tag, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out_tag = res_tag.stdout.read().decode("utf-8")
            out_tag_l = out_tag.split("\n")
            if len(out_tag_l) >= 2 and out_tag_l[-2].startswith('Error response from daemon: No such image:'):
                raise NameError("本地未找到镜像：{}".format(model_repository))
            # 镜像推送私服
            print('镜像开始推送。。。。。。')
            cmd = "docker push " + "27.196.43.168:28081/cspdevkit/aip/" + model_repository
            os.system(cmd)
            res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = res.stdout.read().decode("utf-8")
            # print(out)
            if out:
                flag_text = model_tag + ': digest: sha256:'
                out_l = out.split("\n")
                if not out_l[-2].startswith(flag_text):
                    raise ConnectionError('内部镜像推送至私服失败')
                else:
                    print("镜像上传私服成功")
            # 获取镜像大小
            cmd_size = "docker inspect --format='{{.Size}}' " + model_repository
            res_size = subprocess.Popen(cmd_size, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out_size = res_size.stdout.read().decode("utf-8")
            image_size = convert_bytes(int(out_size.rstrip("'\n").lstrip("'")))

        # 模型服务端注册
        if model_type == "topic":
            url = interface_config["upload"]["model"]
            header = {"Authorization": "Bearer " + user_token}
            params = {"modelSource": model_source, "modelName": model_name,
                      "modelVersion": model_tag, "datasetName": dataset, "size": image_size}
            res = requests.post(headers=header, url=url, data=params)
            res_dict = json.loads(res.text)
        elif model_type == "image":
            url = interface_config["upload"]["image"]
            header = {"Authorization": "Bearer " + user_token}
            params = {"classifyName": image_classify, "imagesType": image_domain, "imagesSource": model_source,
                      "imagesName": model_name, "imagesVersion": model_tag, "size": image_size}
            res = requests.post(headers=header, url=url, data=params)
            res_dict = json.loads(res.text)
        else:
            raise ValueError("镜像类型，topic-业务镜像 image-基础镜像")
        try:
            msg = res_dict["msg"]
        except KeyError as ke:
            msg = res_dict["message"]
        # 服务端返回token过期信息
        if msg == "Invalid access token":
            print(
                "token无效，模型注册失败，请登录，重新上传。登录命令：csp user login (没有账号？使用csp user register 注册一个吧)")
            # 跳转至登录
            # topic_upload(model_repository, model_type, model_source, dataset)
            re_login(topic_upload, image_classify=image_classify, image_domain=image_domain,
                     model_repository=model_repository, model_type=model_type, model_source=model_source,
                     dataset=dataset)
            return

        http_client = HttpClient()
        if res_dict['code'] == 200:
            if model_source == "local" and msg == "模型注册成功":
                print("本地模型注册成功")
                # return
            elif model_source == "cloud" and msg == "模型注册成功":
                print("云端模型注册成功")
                # return
            else:
                raise Exception('error：{}'.format(res_dict))
        else:
            error_res = http_client.error_msg(res_dict)
            raise ConnectionError("注册失败，error_code:{}，message:{}".format(error_res[0], error_res[1]))


def topic_download(model_repository: str):
    user_data = check_user()
    # user_token = user_data["access_token"]
    image_url = check_image_in(model_repository)
    if type(image_url) == str:
        print("开始下载镜像。。。。。")
        cmd = "docker pull " + image_url
        os.system(cmd)
        res_pull = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out_pull = res_pull.stdout.read().decode("utf-8")
        # docker 服务未启动
        if out_pull.startswith("error during connect: This error may indicate that the docker daemon is not running"):
            raise RuntimeError("docker服务未开启")
        if out_pull.replace("\n", "").endswith("http: server gave HTTP response to HTTPS client"):
            raise RuntimeError(
                '''须配置私服地址：vim /etc/docker/daemon.json，增加字段 "insecure-registries": ["27.196.43.168:28081"]. windows系统在Docker Desktop的 Settings-Docker Engine 中配置''')
        # os.system(cmd)
        # print(out_pull)
        # print("镜像下载成功")
    else:
        print("镜像不存在，请检查 ‘镜像资源库：版本号’ 是否正确")


def topic_info(model_repository: str):
    # user_data = check_user()
    # user_token = user_data["access_token"]
    model_name, model_tag = model_repository.split(":")
    http_client = HttpClient()

    interface_config = Configure().data
    url = interface_config["info"]["model"]
    # params = {"classifyName": None, "modelName": model_name, "modelVersion": model_tag}
    params = {"modelName": model_name, "modelVersion": model_tag}
    # res_dict = http_client.get(url, **params)
    # header = {"Authorization": "Bearer " + user_token}
    # res = requests.get(headers=header, url=url, params=params)
    res = requests.get(url=url, params=params)
    res_dict = json.loads(res.text)

    if res_dict['data']:
        res_dict['data']['scoresInfo'] = json.loads(res_dict['data']['scoresInfo'])
    else:
        print('返回值为空')
        error_res = http_client.error_msg(res_dict)
        raise ConnectionError("error_code:{}，message:{}".format(error_res[0], error_res[1]))

    if res_dict["code"] == 200:
        try:
            if res_dict["data"]["scoresInfo"][0].get('ap', None) or res_dict["data"]["scoresInfo"][0].get('ap',
                                                                                                          None) == 0:
                title_dict = {"标签": "category", "召回率": "recall", "准确率": "precision", "ap": "ap"}
            elif res_dict["data"]["scoresInfo"][0].get('fScore', None) or res_dict["data"]["scoresInfo"][0].get(
                    'fScore', None) == 0:
                title_dict = {"标签": "category", "召回率": "recall", "准确率": "precision", "f1": "fScore"}
            elif res_dict["data"]["scoresInfo"][0].get('imageScore', None) or res_dict["data"]["scoresInfo"][0].get(
                    'imageScore', None) == 0:
                title_dict = {"标签": "category", "漏检率": "missingRate", "错误率": "errorRate",
                              "正确率": "correctRate", "分数": "imageScore"}
            else:
                raise KeyError('该评分类型不支持')
            print("name: ", model_repository)
            res_dict = {"data": res_dict["data"]["scoresInfo"]}
            format(res_dict, title_dict)
        except Exception as ae:
            if res_dict["data"]["scoresInfo"] is None:
                print("name: ", model_repository)
                raise ValueError("模型未评估")
            if not res_dict["data"]["scoresInfo"]:
                print("name: ", model_repository)
                raise ValueError('评估结果为空')

            raise ValueError("返回值格式错误")

    else:
        error_res = http_client.error_msg(res_dict)
        raise ConnectionError("error_code:{}，message:{}".format(error_res[0], error_res[1]))


def topic_find(name: str, show=True):
    """
    业务模型模糊查找
    Parameters
    ----------
    name: 查找字符串
    show: 是否以二维表展示信息
    Returns
    -------

    """

    http_client = HttpClient()
    interface_config = Configure().data
    url = interface_config["search"]["model"]
    params = {"name": name}
    res_dict = http_client.get(url, **params)

    title_dict = {"分类": "classifyName", "模型名称": "modelName", "版本": "modelVersion",
                  "评分": "modelScores",
                  "关联数据集": "datasetName", "数据集描述": "funDesc", "作者": "author",
                  "创建时间": "createTime"}

    x = format(res_dict, title_dict, show=show)
    x_string = x.get_string()
    return x_string


def check_image_in(model_repository: str) -> Union[bool, Any]:
    http_client = HttpClient()
    if ":" not in model_repository:
        model_name, model_tag = model_repository, "latest"
    else:
        model_name, model_tag = model_repository.split(":")
    interface_config = Configure().data
    url = interface_config["search"]["docker"]
    params = {"name": model_name, "version": model_tag}
    # header = {"Authorization": "Bearer " + user_token}
    # res = requests.post(headers=header, url=url, data=params)
    res = requests.get(url=url, params=params)
    res_dict = json.loads(res.text)
    if res_dict["code"] == 200:
        try:
            image_url = res_dict["data"]["url"]
            return image_url
        except TypeError as te:
            return False
    else:
        error_res = http_client.error_msg(res_dict)
        raise ConnectionError("error_code:{}，message:{}".format(error_res[0], error_res[1]))


def check_image_out(model_name, model_tag):
    print("连接dockerhub查询中。。。。。。")
    tag_l = []
    size_l = []
    if '/' not in model_name:
        url = 'https://registry.hub.docker.com/v2/repositories/library/' + model_name + '/tags/'
    else:
        url = 'https://registry.hub.docker.com/v2/repositories/' + model_name + '/tags/'
    res = requests.get(url)
    res_out = json.loads(res.text)
    try:
        message = res_out['message']
        print("资源库查找失败，请确认资源库存在且为公开状态。")
        return False
    except KeyError as KE:
        tag_results = res_out['results']
        for result in tag_results:
            tag_l.append(result['name'])
            size_l.append(result['full_size'])
        while res_out['next']:
            url = res_out['next']
            res = requests.get(url)
            res_out = json.loads(res.text)
            tag_results = res_out['results']
            for result in tag_results:
                tag_l.append(result['name'])
                size_l.append(result['full_size'])

            # 基本出现在前两页共20个tag，若遍历所有页，耗时过程，所以在循环体内
            if model_tag not in tag_l:
                print("镜像版本未找到")
                return False, None
            else:
                full_size = size_l[tag_l.index(model_tag)]
                cover_size = convert_bytes(int(full_size))
                return True, cover_size


# 旧版上传，上传物料为tar文件
# def topic_download(name, output):
#     interface_config = Configure().data
#     http_client = HttpClient()
#
#     os.makedirs(output, exist_ok=True)
#
#     url = interface_config["download"]["model"]
#     params = {"name": name}
#     save_path = http_client.download(url, output, **params)
#
#     return save_path


# def model_upload(file_path):
#     pass
#     import requests
#     from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
#
#     file_name = os.path.basename(file_path)
#
#     def my_callback(monitor):
#         progress = (monitor.bytes_read / monitor.len) * 100
#         print("\r 文件上传进度：%d%%(%d/%d)"
#               % (progress, monitor.bytes_read, monitor.len), end=" ")
#
#     e = MultipartEncoder(
#         fields={'model': (file_name, open(file_path, 'rb'), 'application/octet-stream')}
#     )
#
#     m = MultipartEncoderMonitor(e, my_callback)
#     interface_config = Configure().data
#
#     url = interface_config["upload"]["model"]
#
#     r = requests.post(url, data=m, headers={'Content-Type': m.content_type})
#     print(r.text)


# def model_start(name):
#     interface_config = Configure().data
#     http_client = HttpClient()
#
#     url = interface_config["start"]["model"]
#     params = {"modelName": name}
#     res_dict = http_client.post(url, **params)


# def model_eva():
#     pass


# def format_table(string):
#     """
#     优化model list 输出格式
#     Parameters
#     ----------
#     string
#
#     Returns
#     -------
#
#     """
#     s_l_copy = []
#     s_l = string.split("\n")
#     for index, item in enumerate(s_l):
#         s_l_copy.append(item)
#
#         # 判断字符串起始位置特征
#         pattern_start = r'^\|\s*\|'
#         result_start = re.match(pattern_start, item, flags=re.S)
#         if result_start:
#             len_start = len(result_start.group())
#             # 第一格 分割线 替换
#             if s_l[index - 1].startswith("+----"):
#                 res = s_l[index - 1].replace("-", " ", len_start - 2)
#                 res = "|" + res[1:]
#             else:
#                 res = s_l[index - 1]
#
#             # s_l_copy[index - 1] = res
#
#             # 第二格至第五格 分割线 替换
#             j = 0
#             for i in range(len_start - 1, len(res)):
#                 if res[i] == "-":
#                     res = res[:i] + " " + res[i + 1:]
#                 if res[i] == "+":
#                     res = res[:i] + "|" + res[i + 1:]
#                     j += 1
#                 if j >= 5:
#                     break
#
#             # 最后一格 分割线 替换
#             pattern_end = r"\+[\-]*\+$"
#             result_end = re.search(pattern_end, s_l[index - 1], flags=re.S)
#             if result_end:
#                 len_end = len(result_end.group())
#                 s_rep = "| "
#                 for i in range(len_end - 3):
#                     s_rep += " "
#                 s_rep = s_rep + "|"
#                 res = re.sub(pattern_end, s_rep, res)
#
#             s_l_copy[index - 1] = res
#
#     string_new = "\n".join(s_l_copy)
#
#     return string_new


# def drop_list(res):
#     """
#     list 接口返回结果处理
#     Parameters
#     ----------
#     res
#
#     Returns
#     -------
#
#     """
#     res_n = {"data": []}
#     res_data = res["data"]
#     for item in res_data:
#         ms_detail_list = item["msDetailList"]
#         if not ms_detail_list:
#             item_n = {"classifyName": item["classifyName"],
#                       "modelName": item["modelName"],
#                       "modelVersion": item["modelVersion"],
#                       "status": item["status"],
#                       "serviceUrl": item["serviceUrl"],
#                       "module": "",
#                       "datasetNames": "",
#                       "modeScores": "",
#                       "serviceDesc": item["serviceDesc"],
#                       }
#             res_n["data"].append(item_n)
#         else:
#             for index, model in enumerate(ms_detail_list):
#                 if index == 0:
#                     item_n = {"classifyName": item["classifyName"],
#                               "modelName": item["modelName"],
#                               "modelVersion": item["modelVersion"],
#                               "status": item["status"],
#                               "serviceUrl": item["serviceUrl"],
#                               "module": model["module"],
#                               "datasetNames": model["datasetNames"],
#                               "modeScores": model["modeScores"],
#                               "serviceDesc": item["serviceDesc"],
#                               }
#                 else:
#                     item_n = {"classifyName": "",
#                               "modelName": "",
#                               "modelVersion": "",
#                               "status": "",
#                               "serviceUrl": "",
#                               "module": model["module"],
#                               "datasetNames": model["datasetNames"],
#                               "modeScores": model["modeScores"],
#                               "serviceDesc": "",
#                               }
#                 res_n["data"].append(item_n)
#
#     return res_n


# def topic_list(name='', class_name='', show=True):
#     interface_config = Configure().data
#     http_client = HttpClient()
#
#     url = interface_config["list"]["model"]
#     params = {"modelName": name, "classifyName": class_name}
#     res_dict = http_client.get(url, **params)
#
#     res_dict = drop_list(res_dict)
#
#     title_dict = {"主题": "classifyName", "服务名称": "modelName", "版本号": "modelVersion",
#                   "状态": "status", "服务地址": "serviceUrl", "功能": "module", "关联数据集": "datasetNames",
#                   "评分": "modeScores", "服务描述": "serviceDesc"}
#
#     x = format(res_dict, title_dict, show=show)
#     x_string = x.get_string()
#     x_string = format_table(x_string)
#
#     return x_string


if __name__ == '__main__':
    print("start")
