#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/7/01 15:50
# @Author  : liny
# @Site    :
# @File    : Translate_cli.py
# @Software: IDEA
# @python version: 3.7.4
"""

import click
from csp.command.cli import csptools
# from csp.thirdparty import Translate

# 一级命令 CSP translate
@csptools.group("translate")
def translate():
    """
    翻译命令，包括字符字符翻译、文件翻译等子命令

    \b
    csp translate 'commands' -h 获取子命令使用帮助
    """

## 文本翻译
@translate.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-f", "--from_lang", help="源语言, zh-CN: 中文, en：英文等，参考谷歌翻译", required=True)
@click.option("-t", "--to_lang", help="目标语言, zh: 中文, en：英文等，参考谷歌翻译", required=True)
@click.option("-i", "--text", help="待翻译文本", required=True)
@click.option("-m", "--is_merge", help="是否合并返回值",  default=None)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def trans_text(version, port, c_name, r, from_lang, to_lang, text , is_merge,output):
    """
    文本翻译命令

    \b
    使用示例：csp translate trans-text -f 'zh-CN' -t 'en' -i '文本'
    """
    from csp.thirdparty import Translate
    translateclient = Translate(version=version, port=port, c_name=c_name, reload=r)

    result = translateclient.trans_text(from_lang,to_lang,text,is_merge,output)
    print(result)


## 中文翻译为英文
@translate.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--text", help="待翻译中文文本", required=True)
@click.option("-m", "--is_merge", help="是否合并返回值",  default=None)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def text_cn_to_en(version, port, c_name, r, text , is_merge, output):
    """
    中文翻译为英文命令

    \b
    使用示例：csp translate text-cn-to-en -i '文本'
    """
    from csp.thirdparty import Translate
    translateclient = Translate(version=version, port=port, c_name=c_name, reload=r)

    result = translateclient.trans_text_cn_to_en(text,is_merge,output)
    print(result)


## 英文翻译为中文
@translate.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--text", help="待翻译英文文本", required=True)
@click.option("-m", "--is_merge", help="是否合并返回值",  default=None)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def text_en_to_cn(version, port, c_name, r, text , is_merge, output):
    """
    英文翻译为中文命令

    \b
    使用示例：csp translate text-en-to-cn -i 'text'
    """
    from csp.thirdparty import Translate
    translateclient = Translate(version=version, port=port, c_name=c_name, reload=r)

    result = translateclient.trans_text_en_to_cn(text,is_merge,output)
    print(result)


## 文件翻译
@translate.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-f", "--from_lang", help="源语言, zh-CN: 中文, en：英文等，参考谷歌翻译", required=True)
@click.option("-t", "--to_lang", help="目标语言, zh: 中文, en：英文等，参考谷歌翻译", required=True)
@click.option("-i", "--file_path", help="待翻译文件路径（txt）", required=True)
@click.option("-m", "--is_merge", help="是否合并返回值",  default=None)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def trans_file(version, port, c_name, r, from_lang, to_lang, file_path , is_merge,output):
    """
    文件翻译命令

    \b
    使用示例：csp translate trans-file -f 'zh-CN' -t 'en' -i 'txt文件路径'
    """
    from csp.thirdparty import Translate
    translateclient = Translate(version=version, port=port, c_name=c_name, reload=r)

    result = translateclient.trans_file(from_lang,to_lang,file_path,is_merge,output)
    print(result)


## 中文翻译为英文
@translate.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--file_path", help="待翻译中文文件路径（txt）", required=True)
@click.option("-m", "--is_merge", help="是否合并返回值",  default=None)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def file_cn_to_en(version, port, c_name, r, file_path , is_merge, output):
    """
    中文（txt文件）翻译为英文命令

    \b
    使用示例：csp translate file-cn-to-en -i '文件路径'
    """
    from csp.thirdparty import Translate
    translateclient = Translate(version=version, port=port, c_name=c_name, reload=r)

    result = translateclient.trans_file_cn_to_en(file_path,is_merge,output)
    print(result)


## 英文翻译为中文
@translate.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-i", "--file_path", help="待翻译英文文件路径（txt）", required=True)
@click.option("-m", "--is_merge", help="是否合并返回值",  default=None)
@click.option("-o", "--output", help="保存翻译结果（txt文件）的目录，不传则不生成txt文件", default=None)
def file_en_to_cn(version, port, c_name, r, file_path , is_merge, output):
    """
    英文（txt文件）翻译为中文命令

    \b
    使用示例：csp translate file-en-to-cn -i '文件路径'
    """
    from csp.thirdparty import Translate
    translateclient = Translate(version=version, port=port, c_name=c_name, reload=r)

    result = translateclient.trans_file_en_to_cn(file_path,is_merge,output)
    print(result)