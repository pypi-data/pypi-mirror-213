#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/7/05 08:52
# @Author  : liny
# @Site    :
# @File    : labeltool_cli.py
# @Software: IDEA
# @python version: 3.7.4
"""
import click
from csp.thirdparty.labeltool.labeltool_cli import labeltool
from csp.thirdparty.labeltool.doccano.doccano import Doccano

@labeltool.group("doccano")
def doccano():
    """
    doccano工具命令，包括启动、停止、数据导入、数据导出等子命令

    \b
    csp doccano 'commands' -h 获取子命令使用帮助
    """ 
## doccano启动
@doccano.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-c", "--c_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
@click.option('-r', is_flag=True, help="标识符，出现则向后端管理系统请求镜像信息")
@click.option("-u", "--username", help="doccano用户名，默认为admin", default=None)
@click.option("-e", "--email", help="doccano用户邮箱，默认为admin@example.com", default=None)
@click.option("-pwd", "--password", help="doccano用户密码，默认用户名为admin时使用默认密码", default=None)
def start(version, port, c_name, r, username, email, password):
    """
    启动命令

    \b
    使用示例：csp doccano start -u '用户名' -pwd '密码'
    """
    client = Doccano(version=version, port=port, c_name=c_name, reload=r, d_username=username, d_email=email, d_password=password);
    client.start()

## doccano停止
@doccano.command()
@click.option("-v", "--version", help="服务镜像版本，一般不填即可", default=None)
@click.option("-p", "--port", help="容器服务端口，一般不填即可，若存在端口冲突时，用该参数修改", default=None)
@click.option("-cn", "--container_name", help="容器服务名称，一般不填即可，使用默认名称", default=None)
def stop(version, port, c_name):
    """
    停止命令

    \b
    使用示例：csp doccano stop
    """
    client = Doccano(version=version, port=port, c_name=c_name);
    client.stop()

@doccano.command() 
@click.option("--url","-u", help="doccano服务地址， eg.http://127.0.0.1:8000", default="http://127.0.0.1:8000", type=str, show_default=True)
@click.option("--username","-u", help="doccano用户名 eg.admin", default="admin",type=str, show_default=True)
@click.option("--password","-pwd", help="doccano用户密码 eg.password", default="password",type=str, show_default=True)
@click.option("--data_dir","-dd", help="doccano文件目录 eg.data/", default="output/uie",type=str, show_default=True)
@click.option("--file_name","-fn", help="doccano文件名称 eg.doccano_pred.json", default="doccano_pred.json",type=str, show_default=True)
@click.option("--project_type","-pt", help="doccano任务类型 eg.SequenceLabeling", default="SequenceLabeling",type=str, show_default=True)
@click.option("--project_name","-pn", help="doccano任务名称 eg.test", default="test",type=str, show_default=True)
def imp(url,username,password,data_dir,file_name,project_type,project_name):
    """
    数据导入命令

    \b
    使用示例：csp doccano imp --ulr 'http://127.0.0.1:8000' --username '用户名' -pwd '密码' -dd '文件目录' -fn '文件名称' -pt '任务类型' -pn '任务名称'
    """
    Doccano.imp(url, username, password, data_dir, file_name, project_type, project_name) 
    
@doccano.command() 
@click.option("--url","-u", help="doccano服务地址， eg.http://127.0.0.1:8000", default="http://127.0.0.1:8000", type=str, show_default=True)
@click.option("--username","-u", help="doccano用户名 eg.admin", default="admin",type=str, show_default=True)
@click.option("--password","-pwd", help="doccano用户密码 eg.password", default="password",type=str, show_default=True)
@click.option("--project_name","-pn", help="doccano任务名称 eg.test", default="test",type=str, show_default=True)
@click.option("--output_dir","-od", help="导出目录 eg.data/uie", default="output/uie",type=str)
def exp(url,username,password,project_name,output_dir):
    """
    数据导出命令

    \b
    使用示例：csp doccano exp --ulr 'http://127.0.0.1:8000' --username '用户名' -pwd '密码' -pn '任务名称' -od '导出目录'
    """
    Doccano.exp(url, username, password, project_name, output_dir)