#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/27 15:25
# @Author  : xgy
# @Site    : 
# @File    : unst2st_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
from csp.command.cli import csptools
# from csp.thirdparty import Unst2st


# 一级命令 CSPtools unst2st
@csptools.group("unst2st")
def unst2st():
    """
    非结构化转结构化命令，包括纯文本抽取、表格抽取等子命令

    \b
    csp unst2st 'commands' -h 获取子命令使用帮助
    """


## 纯文本抽取
@unst2st.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--file", help="文件路径", required=True)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def extract_text(version, port, c_name, r, file, output):
    """
    纯文本抽取命令

    \b
    支持的文件格式

    \b
    Word格式："DOC"、"doc"、 "DOCX"、 "docx"，"DOCM"，"docm"，"WPS"，"wps"
    Excel格式："XLS"，"xls"，"XLSX"，"xlsx"，"ET"，"et"；
    PDF格式："PDF"，"pdf"；
    CSV格式："CSV"，"csv"；
    OFD格式："OFD"，"ofd"；
    CEB格式："CEB"，"ceb"

    \b
    使用示例：csp unst2st extract-text -i '文件路径'
    """
    from csp.thirdparty import Unst2st
    unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
    result = unst2st.extract_text(file, output)
    print(result)


## 去水印
@unst2st.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--in_file", help="带水印pdf文件路径", required=True)
@click.option("-o", "--output", help="去水印后文件保存目录", required=True)
def remove_watermark(version, port, c_name, r, in_file, output):
    """
    pdf文件去水印命令

    \b
    使用示例：csp unst2st remove-watermark -i 'pdf文件路径' -o '去水印后文件保存目录'
    """
    from csp.thirdparty import Unst2st
    unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
    unst2st.remove_watermark(in_file, output)

# 抽取图片文本
# @unst2st.command()
# @click.option("-v", "--version", help="the version of server images", required=True)
# @click.option("-p", "--port", help="the port for server container", required=True)
# @click.option("-c", "--c_name", help="the container name", required=True, default=None)
# @click.option('-r', is_flag=True, help="Re query image information.Indicates true when it appears")
# @click.option("-i", "--file", help="the input file", required=True)
# @click.option("-o", "--output", help="the folder to save output txt file", default=None)
# def extract_img_txt(version, port, c_name, r, file, output):
#     """
#     CSPTools unst2st extract_img_txt line
#     """
#     unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
#     result = unst2st.extract_img_txt(file, output)
#     print(result)


# 表格提取
@unst2st.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--file", help="待抽取文本路径", required=True)
@click.option("-o", "--output", help="抽取结果（txt文件目录）", default=None)
def extract_table(version, port, c_name, r, file, output):
    """
    从文档抽取表格命令

    \b
    支持的文件格式

    \b
    Word格式："DOC"、"doc"、 "DOCX"、 "docx"，"WPS"，"wps"
    Excel格式："XLS"，"xls"，"XLSX"，"xlsx"
    PDF格式："PDF"，"pdf"

    \b
    使用示例：csp unst2st extract-table -i '待抽取文本路径' -o '结果保存目录'
    """
    from csp.thirdparty import Unst2st
    unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
    result = unst2st.extract_table(file, output)
    print(result)


# 篇章段落提取
@unst2st.command()
@click.option("-v", "--version", help="the version of server images", default=None)
@click.option("-p", "--port", help="the port for server container", default=None)
@click.option("-c", "--c_name", help="the container name", default=None)
@click.option('-r', is_flag=True, help="Re query image information.Indicates true when it appears")
@click.option("-i", "--file", help="待抽取文本路径", required=True)
@click.option("-o", "--output", help="抽取结果（txt文件目录）", default=None)
def extract_structure(version, port, c_name, r, file, output):
    """
    从文档抽取段落内容命令

    \b
    支持的文件格式

    \b
    Word格式："DOC"、"doc"、 "DOCX"、 "docx"，"WPS"，"wps"
    PDF格式："PDF"，"pdf"；

    \b
    使用示例：csp unst2st extract-structure -i '待抽取文本路径' -o '结果保存目录'
    """
    from csp.thirdparty import Unst2st
    unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
    result = unst2st.extract_structure(file, output)
    print(result)


if __name__ == '__main__':
    print("start")
